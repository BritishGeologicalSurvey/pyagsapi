/***************************************************************************

"THE BEER-WARE LICENSE":
<ivan@sanchezortega.es> wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.

***************************************************************************/

/**
 * @class L.FeatureGroup.OGCAPI
 *
 * Client implementation for OGC API Features.
 *
 * Currently implements:
 * - Core (part 1)
 *   - bbox: Reloads data from the OGC API endpoint whenever the map viewport changes
 *     (i.e. on center/zoom change)
 *   - bounds: Loads from metadata, and returns it when `getBounds()` is called.
 *   - attribution: Reads it and applies it to loaded features. Meaning that
 *     attribution doesn't show if zero features are visible on the viewport.
 *
 * Initialization requires the **collections** endpoint and the name of
 * the desired collection, e.g.:
 *
 * ```
 * L.featureGroup.ogcApi("http://maps.ecere.com/ogcapi/collections/", {
 *    collection: "SanDiegoCDB:Trees")
 * }).addTo(map);
 * ```
 *
 * Despite the `FeatureGroup` name, this inherits from `L.GeoJSON`. This means
 * that there's `style` and `pointToLayer` options for styling the data.
 *
 */

L.FeatureGroup.OGCAPI = L.GeoJSON.extend({
	options: {
		/**
		 * @option limit = 100
		 * The maximum amount of features to have on the map at any given time.
		 */
		limit: 400,

		/**
		 * @option padding: Number = 0.1
		 * How much to extend the query bbox outside of the map view.
		 * e.g. 0.1 would be 10% of map view in each direction
		 *
		 * Larger values means fewer reloads (the data is only re-queried when
		 * the viewable bbox is not entirely within the bbox of the queried data),
		 * but requests more data from the service (risking hitting the `limit`
		 * earlier).
		 */
		padding: 0.1,

		/**
		 * @option collection: String = undefined
		 * Named of the desired collection.
		 */
	},

	initialize: function (endpoint, options) {
		L.FeatureGroup.prototype.initialize.call(this, [], options);

		// Strip the trailing slash, if there's one; then add '/collections' to it.
		collectionsURL = new URL(
			endpoint.replace(/\/?$/, "") + "/collections",
			document.URL
		);

		this._bbox = L.latLngBounds([]);
		this._dataBounds = L.latLngBounds([]);

		this._req = Promise.resolve();
		this._abortController = new AbortController();

		// Code for this._collection is duplicated from L.ImageOverlay.OGCAPI
		/// TODO: Deduplicate!!!
		const collection = this.options.collection;
		this._collection = fetch(collectionsURL, {
			headers: {
				Accept: "application/json",
			},
		})
			.then((response) => response.json())
			.then((json) => {
				// console.log(json.collections);
				const matches = json.collections.filter((c) => c.id === collection);
				if (matches.length === 0) {
					throw new Error(
						`Collection '${collection}' is not available from OGC API endpoint ${this._baseURL}`
					);
				} else if (matches.length > 1) {
					throw new Error(
						`Collection '${collection}' has a duplicate definition from OGC API endpoint ${this._baseURL}`
					);
				}

				const collectionData = matches[0];

				// TODO: There are some XSS concerns about pulling API-provided
				// HTML as attribution without sanitizing the HTML first.
				if ("attribution" in collectionData) {
					this.options.attribution = collectionData.attribution;
				}

				// Filter links to find the endpoint for features in geojson format
				// NOTE: 'items' should be changed into 'http://www.opengis.net/def/rel/OGC/1.0/items'
				// as the spec goes final. See https://github.com/opengeospatial/ogcapi-features/issues/311
				/// FIXME: An en dpoint might be able to accept multiple MIME types,
				/// and the logic for selecting the preferred one is not trivial.
				const links = collectionData.links.filter(
					(l) => l.rel === "items" && l.type === "application/geo+json"
				);

				if (links.length === 0) {
					throw new Error(
						"OGC API: Features for collection are not available in GeoJSON"
					);
				} else if (links.length > 1) {
					throw new Error(
						"OGC API: Features for collection have multiple endpoints for GeoJSON"
					);
				}

				this._endpoint = new URL(links[0].href, collectionsURL);

				/// Note: the OGC API Common specs (section 8.4.2) says
				/// "[bbox] provides *a set* of rectangular bounding boxes [....]
				/// Typically only the first [would] be populated."
				const bbox = collectionData.extent.spatial.bbox[0];

				this._dataBounds = L.latLngBounds([
					[bbox[1], bbox[0]],
					[bbox[3], bbox[2]],
				]);

				/**
				 * @event ready
				 * Fired whenever the collection metadata has been loaded.
				 */
				this.fire("ready");
				this._onReady();
			});
	},

	getBounds: function () {
		return this._dataBounds;
	},

	onAdd: function (map) {
		L.FeatureGroup.prototype.onAdd.apply(this, arguments);
		this.once("ready", this._onReady, this);
		this._onMapMoveEnd();
	},

	_onReady: function (ev) {
		this._map.on("moveend", this._onMapMoveEnd, this);
		this._map.on("zoomstart", this._onMapZoomStart, this);
	},

	onRemove: function (map) {
		this.off("ready", this._onReady, this);
		this._map.off("moveend", this._onMapMoveEnd, this);
		this._map.off("zoomstart", this._onMapZoomStart, this);
		L.FeatureGroup.prototype.onRemove.apply(this, arguments);
	},

	_onMapZoomStart: function (ev) {
		// Invalidate viewable bounds, so stuff gets reloaded on the next
		// `modeend` event.
		this._bbox = L.latLngBounds([]);
	},

	_onMapMoveEnd: function (ev) {
		var mapBounds = this._map.getBounds();

		if (this._bbox.isValid() && this._bbox.contains(mapBounds)) {
			return;
		}

		this._bbox = mapBounds.pad(this.options.padding);

		// 		this.clearLayers();
		// 		this.addLayer(L.rectangle(this._bbox));
		// 		console.log('new bbox:', this._bbox.toBBoxString());

		const south = this._bbox.getSouth();
		const north = this._bbox.getNorth();
		const west = this._bbox.getWest();
		const east = this._bbox.getEast();

		const params = this._endpoint.searchParams;
		params.set("bbox", `${west},${south},${east},${north}`);
		params.set("limit", this.options.limit);

		this._abortController.abort();
		this._abortController = new AbortController();

		this._req = fetch(this._endpoint, {
			signal: this._abortController.signal,
			headers: {
				Accept: "application/geo+json, application/json",
			},
		})
			.then((res) => res.json())
			.then((geojson) => {
				/// FIXME: This should not delete features which are already in
				/// the data. Instead, this should filter
				this.clearLayers();
				this.addData(geojson);
			});
	},

	/**
	 * @section CRUD methods
	 * The following methods implement part 4 of the OGC API Features.
	 *
	 * Note that the user interface for this methods needs to be implemented
	 * separately.
	 *
	 * @method createFeature(feature: Object): Promise to Response
	 * Expects a GeoJSON feature (conformant to the collection schema),
	 * and returns a `Promise`.
	 *
	 * The `Promise` is akin to a `Response`, as in the `fetch` API. Note that
	 * the result code of that response might be either 201 or 202, and that
	 * a 202 response code means that the feature hasn't been added
	 * instantaneously.
	 */
	createFeature(feature) {
		/// FIXME: This goes against the URLs in the metadata!!!!
		this._endpoint.searchParams.delete("f", this.options.limit);

		this._endpoint.searchParams.delete("bbox");
		this._endpoint.searchParams.delete("limit");

		return fetch(this._endpoint, {
			method: "POST",
			body: JSON.stringify(feature),
			headers: {
				"Content-Type": "application/geo+json",
				Accept: "application/geo+json, application/json",
			},
		});
	},

	/**
	 * @method replaceFeature(feature: Object): Promise to Response
	 * Akin to `createFeature`, but expects the feature to have a `id`
	 * property. The feature with that ID shall be modified.
	 */
	replaceFeature(feature) {
		/// FIXME: This goes against the URLs in the metadata!!!!
		this._endpoint.searchParams.delete("f", this.options.limit);

		this._endpoint.searchParams.delete("bbox");
		this._endpoint.searchParams.delete("limit");

		/// FIXME!!! This just *assumes* things about the URL structure.
		/// It would be nice to be able to fetch the URL for each feature
		/// in a more reliable way.
		const featureURL = new URL(this._endpoint);
		featureURL.pathname += `/${feature.id}`;

		/// FIXME!! Include the `If-Match` header with the known `ETag`

		return fetch(featureURL, {
			method: "PUT",
			body: JSON.stringify(feature),
			headers: {
				"Content-Type": "application/geo+json",
				Accept: "application/geo+json, application/json",
			},
		});
	},

	/**
	 * @method deleteFeature(feature: Object): Promise to Response
	 * Akin to `createFeature`, but deletes an existing feature instead.
	 * As `replaceFeature`, the feature must have a `id` property in its
	 * GeoJSON representation.
	 */
	deleteFeature(feature) {
		/// FIXME: This goes against the URLs in the metadata!!!!
		this._endpoint.searchParams.delete("f", this.options.limit);

		this._endpoint.searchParams.delete("bbox");
		this._endpoint.searchParams.delete("limit");

		/// FIXME!!! This just *assumes* things about the URL structure.
		/// It would be nice to be able to fetch the URL for each feature
		/// in a more reliable way.
		const featureURL = new URL(this._endpoint);
		featureURL.pathname += `/${feature.id}`;

		return fetch(featureURL, {
			method: "DELETE",
			//body: JSON.stringify(feature),
			headers: {
				"Content-Type": "application/geo+json",
				Accept: "application/geo+json, application/json",
			},
		});
	},

	/**
	 * TODO: implement updateFeature
	 * It *should* send a `fetch` request with the PATCH method, and
	 * in the payload **only** the bits of the GeoJSON structure that need to be
	 * changed.
	 */
	updateFeature(feature) {
		throw new Error("Unimplemented");
	},
});

L.featureGroup.ogcApi = function ogcApi(endpoint, options) {
	return new L.FeatureGroup.OGCAPI(endpoint, options);
};
