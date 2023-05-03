
var control = {};
var overlays = {};
var baseMaps = {};

var mapCentre = [54.5, -1.5];
var initZoom = 6;


/** Create the map instance - when the leaflet js is included */
var map = L.map('mapid',
    {
        center: mapCentre, // centre at specified coords
        zoom: initZoom
    }
);


/** Use the L.tileLayer.betterWms extension to load the wms layer */
geologyOfbtn = L.tileLayer.betterWms('http://ogc.bgs.ac.uk/cgi-bin/BGS_Bedrock_and_Superficial_Geology/wms?', {
    layers: 'GBR_BGS_625k_BLS,GBR_BGS_625k_SLS',
    tiled: true,
    format: 'image/png',
    transparent: true,
    opacity: 0.7,
    continuousWorld: true,
    zIndex: 1000

}).addTo(map);

/** Add Esri basemap layers to map - this is using the esri-leaflet.js extension 
 * for Leaflet and makes it easier to include Esri functionality in to Leaflet maps: https://esri.github.io/esri-leaflet   */
var topo = L.esri.basemapLayer("Topographic");
var imagery = L.esri.basemapLayer("Imagery").addTo(map);

var agsindex = L.tileLayer.wms('https://map.bgs.ac.uk/arcgis/services/AGS/AGS_Export/MapServer/WMSServer?', {
    layers: 'Boreholes',
    format: 'image/png',
    transparent: true,
    attribution: "AGS Data from British Geological Survey",
    zIndex: 1001
}).addTo(map);

(async () => {
    const airports = await fetch('https://demo.ldproxy.net/zoomstack/collections/airports/items?limit=100', {
      headers: {
        'Accept': 'application/geo+json'
      }
    }).then(response => response.json());
    const iconurl = 'data:image/svg+xml;base64,'+btoa('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect width="200" height="200" rx="24" fill="#000"/><path d="M 91.268,28.17 C 91.308,16.432 109.015,16.432 109.015,28.514 L 109.015,77.831 L 178.023,119.336 L 178.023,137.549 L 109.319,114.945 L 109.319,151.776 L 125.205,164.221 L 125.205,178.61 L 100.698,171.001 L 76.191,178.61 L 76.191,164.221 L 91.915,151.776 L 91.915,114.945 L 23.191,137.549 L 23.191,119.336 L 91.248,77.831 L 91.248,28.17 z" fill="#fff"/></svg>');
    L.geoJSON(airports, {
      pointToLayer: function (feature, latlng) {
        return L.marker(latlng, { 
          icon: L.icon({
            iconUrl: iconurl,
            iconSize: [20, 20],
            iconAnchor: [10, 10],
            popupAnchor: [0, -10]
          })
        });
      },
      onEachFeature: onEachFeature
    }).addTo(map);
})();    

function onEachFeature(feature, layer) {
    var popupContent = "<a href='https://demo.ldproxy.net/zoomstack/collections/airports/items/" + feature.id + "' target='_blank'>" + feature.properties.name + "</a>";
    if (feature.properties && feature.properties.popupContent) {
        popupContent += feature.properties.popupContent;
    }
    layer.bindPopup(popupContent);
}

// var agsboreholes = L.featureGroup
// .ogcApi("https://ogcapi.bgs.ac.uk/", {
//     collection: "agsboreholeindex",
//     onEachFeature: function (feat, layer) {
//         var properties = feat.properties;
//         var popupContent = "<b>AGS Borehole Information</b><br><hr>" +
//             "<b>BGS LOCA ID: </b>" + properties.bgs_loca_id + "<br>" +
//             "<b>Depth (m): </b>" + properties.loca_fdep + "<br>" +
//             "<b>Project Name: </b>" + properties.proj_name + "<br>" +
//             "<b>Project Engineer: </b>" + properties.proj_eng + "<br>" +
//             "<b>Project Contractor: </b>" + properties.proj_cont + "<br>" +
//             "<b>Original LOCA ID: </b>" + properties.loca_id + "<br>" +
//             "<b>AGS Graphical Log: </b>" + "<a href=" + "https://agsapi.bgs.ac.uk/ags_log/?bgs_loca_id=" + properties.bgs_loca_id + " target=" + "_blank" + ">View</a>" + "<br>" +
//             "<b>AGS Submission Record (raw data): </b>" + "<a href=" + properties.dad_item_url + " target=" + "_blank" + ">View</a>" + "<br>";
//         layer.bindPopup(popupContent);
//     },
// }).addTo(map);

baseMaps["<span>Topographic</span>"] = topo;
baseMaps["<span>Imagery</span>"] = imagery;
overlays["<span>Geology</span>"] = geologyOfbtn;
overlays["<span>AGS Index</span>"] = agsindex;
// overlays["<span>AGS Info</span>"] = agsboreholes;

control = L.control.layers(baseMaps, overlays, { collapsed: true }).addTo(map);

// jQuery UI slider for controling the opacity of the wms layer.
$opacitySlider = $("#opacitySlider").slider({
    slide: function (event, ui) {
        geologyOfbtn.setOpacity((ui.value / 100).toFixed(1));
    },
    min: 0,
    max: 100,
    step: 10,
    value: 70
});

// diable dragging when entering div 
$("#dOpacitySliderBox").on('mouseover', function () {
    map.dragging.disable();
});

// Re-enable dragging when leaving div
$("#dOpacitySliderBox").on('mouseout', function () {
    map.dragging.enable();
});

$("#dOpacitySliderBox").click(false);


/** Find users location and move map to that position 
 * - this is using the broswer location services so is not alway accurate on a desktop computer */
map.locate({ setView: true, maxZoom: 16 });


/** Add circle at current location when location has been found*/
function onLocationFound(e) {
    var radius = e.accuracy / 2;
    var message = "accuracy: " + e.accuracy
        + "M<br />time: " + e.timestamp
        + "<br />Lat: " + e.latitude
        + "<br />Lng: " + e.longitude;

    L.circle(e.latlng, radius).addTo(map).bindPopup(message);
}

map.on('locationfound', onLocationFound);


/** Geocoder search functionality - this is using Esri's location search functionality: 
 * https://esri.github.io/esri-leaflet/examples/geocoding-control.html */
var searchControl = L.esri.Geocoding.geosearch().addTo(map);
var results = L.layerGroup().addTo(map);

searchControl.on('results', function (data) {
    results.clearLayers();
    // do something with the search results
});

// agsboreholes.once("ready", function (ev) {
//     map.fitBounds(agsboreholes.getBounds());
// });
