// validation-map.js
var vMap={};

vMap.colours=['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928'];

vMap.map={
    "basemaps":{},
    "lyrs":{},
    "lMap":{},
    "control":{},
    "drawCtrl":{}
    };

vMap.setupValidationMap=function(){
    console.log("vMap.setupValidationMap");
    var baseLayers={};
    var overlays={};
    var mapOpts={
        "zoom":6,
        "minZoom":5,
        "maxZoom":18,
        "center":[54.5,-1.5]
        };
    // create Leaflet map
    vMap.map.lMap=L.map("res_Map",mapOpts);
    // add Esri basemap layers to map - this is using the esri-leaflet.js extension
    vMap.map.basemaps.topo=L.esri.basemapLayer("Topographic").addTo(vMap.map.lMap);
    vMap.map.basemaps.imagery=L.esri.basemapLayer("Imagery");
    // add layer selection control
    baseLayers["<span>Topographic</span>"]=vMap.map.basemaps.topo;
    baseLayers["<span>Imagery</span>"]=vMap.map.basemaps.imagery;
    vMap.map.control=L.control.layers(baseLayers,overlays,{"collapsed":false}).addTo(vMap.map.lMap);
    // add placeholder featureGroup for GeoJSON markers (layer per file)
    vMap.map.lyrs["GeoJSON"]=L.featureGroup().addTo(vMap.map.lMap);
    // ...
    return true;
    };

vMap.showOnValidationMap=function(geoJSON,fileName,ix){
    console.log("vMap.showOnValidationMap");
    console.log(geoJSON);
    console.log(fileName);
    console.log(ix);
    // show GeoJSON features on map - add popups and tooltips
    L.geoJSON(geoJSON,{
        "pointToLayer":function(feature,latlng){
            return vMap.pointToLayer(feature,latlng,ix);
            },
        "onEachFeature":function(feature,layer){
            layer.bindTooltip(feature.properties.LOCA_ID);
            layer.bindPopup(vMap.getPopupContent(feature,fileName));
            }
        }).addTo(vMap.map.lyrs.GeoJSON);
    return true;
    };

vMap.fitValidationMap=function(){
    console.log("vMap.fitValidationMap");
    // force map redraw
    vMap.map.lMap.invalidateSize();
    // fit bounds of validation GeoJSON layer(s)
    vMap.map.lMap.fitBounds(vMap.map.lyrs.GeoJSON.getBounds());
    return true;
    };

vMap.getPopupContent=function(feature,fileName){
    // generate marker popup HTML
    var popupContent="";
    var popupFields=["line_no","LOCA_ID","LOCA_FDEP","PROJ_NAME","PROJ_ENG","PROJ_CONT"];
    var popupLabels=["Line","Original LOCA ID","Depth (m)","Project Name","Project Engineer","Project Contractor"];
    var popupField="";
    var popupLabel="";
    var i=0;
    popupContent=popupContent + "<span class='popupContent'>";
    popupContent=popupContent + "<h4>AGS Borehole Information</h4>";
    popupContent=popupContent + "<label>File</label> : <strong>" + fileName + "</strong><br />";
    for(i=0;i < popupFields.length;i++){
        popupField=popupFields[i];
        popupLabel=popupLabels[i];
        popupContent=popupContent + "<label>" + popupLabel + "</label> : <strong>" + feature.properties[popupField] + "</strong><br />";
        };
    popupContent=popupContent + "</span>";
    return popupContent;
    };

vMap.pointToLayer=function(feature,latlng,ix){
    // generate circleMarker for a feature, colour set by ix (file index in results)
    var markerOpts={
        "id":feature.properties.LOCA_ID,
        "radius":6,
        "fillColor":vMap.colours[ix],
        "color":"#000",
        "weight":1,
        "opacity":1,
        "fillOpacity":0.7,
        "stroke":false
        };
    var marker=L.circleMarker(latlng,markerOpts);
    return marker;
    };

vMap.resetValidationMap=function(){
    console.log("vMap.resetValidationMap");
    // force map redraw when showing map and clear out any existing layers
    vMap.map.lyrs.GeoJSON.clearLayers();
    vMap.map.lMap.invalidateSize();
    $("#res_MapFrame").show();
    return true;
    };

vMap.hideValidationMap=function(){
    // hide validation map (when no GeoJSON in results)
    $("#res_MapFrame").hide();
    return true;
    };

