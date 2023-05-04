
var control = {};
var overlays = {};
var baseMaps = {};

var mapCentre = [54.5, -1.5];
var initZoom = 5.5;


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
    opacity: 0.5,
    continuousWorld: true,
    zIndex: 1000

}).addTo(map);

// /** Use the L.tileLayer.betterWms extension to load the 50k wms layer */
// 50kgeology = L.tileLayer.betterWms('https://map.bgs.ac.uk/arcgis/services/BGS_Detailed_Geology/MapServer/WMSServer?', {
//     layers: 'BGS.50k.Bedrock,BGS.50k.Superficial.deposits,BGS.50k.Linear.features',
//     tiled: true,
//     format: 'image/png',
//     transparent: true,
//     opacity: 0.7,
//     continuousWorld: true,
//     zIndex: 1000

// }).addTo(map);

/** Add Esri basemap layers to map - this is using the esri-leaflet.js extension 
 * for Leaflet and makes it easier to include Esri functionality in to Leaflet maps: https://esri.github.io/esri-leaflet   */
var topo = L.esri.basemapLayer("Topographic");
var imagery = L.esri.basemapLayer("Imagery").addTo(map);

/** Use the L.tileLayer.betterWms extension to load the AGS wms layer */
var agsindex = L.tileLayer.wms('https://map.bgs.ac.uk/arcgis/services/AGS/AGS_Export/MapServer/WMSServer?', {
    layers: 'Boreholes',
    format: 'image/png',
    transparent: true,
    attribution: "AGS Data from British Geological Survey",
    zIndex: 1001
}).addTo(map);

/** Use the Leaflet.FeatureGroup.OGCAPI.js extension to load the AGS OGCAPI-Features layer */
var agsboreholes = L.featureGroup
.ogcApi("https://ogcapi.bgs.ac.uk/", {
    collection: "agsboreholeindex",
    onEachFeature: function (feat, layer) {
        var properties = feat.properties;
        var popupContent = "<b>AGS Borehole Information</b><br><hr>" +
            "<b>BGS LOCA ID: </b>" + properties.bgs_loca_id + "<br>" +
            "<b>Depth (m): </b>" + properties.loca_fdep + "<br>" +
            "<b>Project Name: </b>" + properties.proj_name + "<br>" +
            "<b>Project Engineer: </b>" + properties.proj_eng + "<br>" +
            "<b>Project Contractor: </b>" + properties.proj_cont + "<br>" +
            "<b>Original LOCA ID: </b>" + properties.loca_id + "<br>" +
            "<b>AGS Graphical Log: </b>" + "<a href=" + "https://agsapi.bgs.ac.uk/ags_log/?bgs_loca_id=" + properties.bgs_loca_id + " target=" + "_blank" + ">View</a>" + "<br>" +
            "<b>AGS Data: </b>" + "<a href=" + "https://agsapi.bgs.ac.uk/ags_export/?bgs_loca_id=" + properties.bgs_loca_id + " target=" + "_blank" + ">Download</a>" + "<br>" +
            "<b>AGS Submission Record (raw data): </b>" + "<a href=" + properties.dad_item_url + " target=" + "_blank" + ">View</a>" + "<br>";
        layer.bindPopup(popupContent);
    },
});

agsboreholes.once("ready", function (ev) {
    map.fitBounds(agsboreholes.getBounds());
});


// (async () => {
//     const agsboreholes = await fetch('https://ogcapi.bgs.ac.uk/collections/agsboreholeindex/items?bbox=' + map.getBounds().toBBoxString() + '&limit=100', {
//       headers: {
//         'Accept': 'application/geo+json'
//       }
//     }).then(response => response.json());
//     L.geoJSON(agsboreholes, {
//       onEachFeature: onEachFeature
//     }).addTo(map);
// })();    

// function onEachFeature(feature, layer) {
//     var popupContent = "<b>AGS Borehole Information</b><br><hr>" +
//             "<b>BGS LOCA ID: </b>" + feature.properties.bgs_loca_id + "<br>" +
//             "<b>Depth (m): </b>" + feature.properties.loca_fdep + "<br>" +
//             "<b>Project Name: </b>" + feature.properties.proj_name + "<br>" +
//             "<b>Project Engineer: </b>" + feature.properties.proj_eng + "<br>" +
//             "<b>Project Contractor: </b>" + feature.properties.proj_cont + "<br>" +
//             "<b>Original LOCA ID: </b>" + feature.properties.loca_id + "<br>" +
//             "<b>AGS Graphical Log: </b>" + "<a href=" + "https://agsapi.bgs.ac.uk/ags_log/?bgs_loca_id=" + feature.properties.bgs_loca_id + " target=" + "_blank" + ">View</a>" + "<br>" +
//             "<b>AGS Data: </b>" + "<a href=" + "https://agsapi.bgs.ac.uk/ags_export/?bgs_loca_id=" + feature.properties.bgs_loca_id + " target=" + "_blank" + ">Download</a>" + "<br>" +
//             "<b>AGS Submission Record (raw data): </b>" + "<a href=" + feature.properties.dad_item_url + " target=" + "_blank" + ">View</a>" + "<br>";
//     if (feature.properties && feature.properties.popupContent) {
//         popupContent += feature.properties.popupContent;
//     }
//     layer.bindPopup(popupContent);
// }

baseMaps["<span>Topographic</span>"] = topo;
baseMaps["<span>Imagery</span>"] = imagery;
overlays["<span>Geology</span>"] = geologyOfbtn;
overlays["<span>AGS Index</span>"] = agsindex;
overlays["<span>AGS Details</span>"] = agsboreholes;

control = L.control.layers(baseMaps, overlays, { collapsed: false }).addTo(map);

// jQuery UI slider for controling the opacity of the wms layer.
$opacitySlider = $("#opacitySlider").slider({
    slide: function (event, ui) {
        geologyOfbtn.setOpacity((ui.value / 100).toFixed(1));
    },
    min: 0,
    max: 100,
    step: 10,
    value: 50
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


/** Geocoder search functionality - this is using Esri's location search functionality: 
 * https://esri.github.io/esri-leaflet/examples/geocoding-control.html */
var searchControl = L.esri.Geocoding.geosearch().addTo(map);
var results = L.layerGroup().addTo(map);

searchControl.on('results', function (data) {
    results.clearLayers();
    // do something with the search results
});
