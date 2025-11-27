L.TileLayer.BetterWMS = L.TileLayer.WMS.extend({

  onAdd: function (map) {
    // Triggered when the layer is added to a map.
    //   Register a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onAdd.call(this, map);
    map.on('click', this.getFeatureInfo, this);
  },

  onRemove: function (map) {
    // Triggered when the layer is removed from a map.
    //   Unregister a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onRemove.call(this, map);
    map.off('click', this.getFeatureInfo, this);
  },

  getFeatureInfo: function (evt) {
    // Make an AJAX request to the server and hope for the best
    var url = this.getFeatureInfoUrl(evt.latlng),
        showResults = L.Util.bind(this.showGetFeatureInfo, this);
    $.ajax({
      url: url,
      success: function (data, status, xhr) {
        var err = typeof data === 'string' ? null : data;
        showResults(err, evt.latlng, data);
      },
      error: function (xhr, status, error) {
        showResults(error);
      }
    });
  },

  getFeatureInfoUrl: function (latlng) {
    // Construct a GetFeatureInfo request URL given a point
    var point = this._map.latLngToContainerPoint(latlng, this._map.getZoom()),
        size = this._map.getSize(),

        params = {
          request: 'GetFeatureInfo',
          service: 'WMS',
          srs: 'EPSG:4326',
          styles: this.wmsParams.styles,
          transparent: this.wmsParams.transparent,
          version: this.wmsParams.version,
          format: this.wmsParams.format,
          bbox: this._map.getBounds().toBBoxString(),
          height: size.y,
          width: size.x,
          layers: this.wmsParams.layers,
          query_layers: this.wmsParams.layers,
          info_format: 'text/html'
        };

    params[params.version === '1.3.0' ? 'i' : 'x'] = point.x;
    params[params.version === '1.3.0' ? 'j' : 'y'] = point.y;

    return this._url + L.Util.getParamString(params, this._url, true);
  },

  showGetFeatureInfo: function (err, latlng, content) {
    // do nothing if there's an error
    if (err) { console.log(err); return; }
    // do nothing if WMS popup disabled
    if (!agsMap.drawing.showWMSpopup) { return; }

    // otherwise show the filtered content in a popup
    const allowedFields = ['LEX_RCS', 'LEX_RCS_D', 'BGSTYPE', 'MAX_TIME_D'];
    let filteredHTML = '';

    // Parse the HTML response
    const parser = new DOMParser();
    const doc = parser.parseFromString(content, 'text/html');

    // Get all tables and their titles
    const tables = doc.querySelectorAll('table');
    const titles = doc.querySelectorAll('h5');

    tables.forEach((table, index) => {
      const headers = table.querySelectorAll('th');
      const values = table.querySelectorAll('td');

      let filteredHeaders = [];
      let filteredValues = [];

      headers.forEach((header, i) => {
        const key = header.textContent.trim();
        const value = values[i] ? values[i].textContent.trim() : '';
        if (allowedFields.includes(key)) {
          filteredHeaders.push(key);
          filteredValues.push(value);
        }
      });

      if (filteredHeaders.length > 0) {
        const titleText = titles[index].textContent.replace(/^.*?(BGS\.[\w\.]+)/, '$1').replace(/'$/, '').trim();
        filteredHTML += `<h4>${titleText}</h4>`;
        filteredHTML += `<table class="popup-table">
                            <thead><tr>${filteredHeaders.map((h) => `<th>${h}</th>`).join('')}</tr></thead>
                            <tbody><tr>${filteredValues.map((v) => `<td>${v}</td>`).join('')}</tr></tbody>
                          </table><br>`;
      }
    });

    if (!filteredHTML) {
      filteredHTML = '<p>No detailed information available for this feature.</p>';
    }

    L.popup({ maxWidth: 500 })
      .setLatLng(latlng)
      .setContent(filteredHTML)
      .openOn(this._map);
  }
});

L.tileLayer.betterWms = function (url, options) {
  return new L.TileLayer.BetterWMS(url, options);
};