var agsMap={};

agsMap.init=function(){
    agsMap.hideModalBtn();
    $("#closeModalBtn").on("click",agsMap.hideModalBtn);
    $("#ags_data").on("click","input.checkPolyBtn",agsMap.checkPoly);
    agsMap.setupMap();
    return true;
    };

agsMap.hideModalBtn=function(){
    $("#extentModal").hide();
    return true;
    };

agsMap.map={
    "basemaps":{},
    "lyrs":{},
    "lMap":{},
    "control":{},
    "drawCtrl":{}
    };

agsMap.polyData={};
agsMap.maxBoresForDownload=10;

agsMap.setupMap=function(){
    var baseLayers={};
    var overlays={};
    var mapOpts={
        "zoom":6,
        "minZoom":5,
        "maxZoom":18,
        "center":[54.5,-1.5]
        };

    // create Leaflet map
    agsMap.map.lMap=L.map("mapid",mapOpts);

    // add Esri basemap layers to map - this is using the esri-leaflet.js extension
    agsMap.map.basemaps.topo=L.esri.basemapLayer("Topographic").addTo(agsMap.map.lMap);
    agsMap.map.basemaps.imagery=L.esri.basemapLayer("Imagery");

    // use the L.tileLayer.betterWms extension to load the 50k wms layer
    agsMap.map.lyrs.geologyOfbtn=L.tileLayer.betterWms("https://ogc.bgs.ac.uk/cgi-bin/BGS_Bedrock_and_Superficial_Geology/wms?", {
        "layers": 'GBR_BGS_625k_BLS,GBR_BGS_625k_SLS',
        "tiled": true,
        "format": 'image/png',
        "transparent": true,
        "opacity": 0.5,
        "continuousWorld": true,
        "zIndex": 1000
        }).addTo(agsMap.map.lMap);

    // Use the L.tileLayer.betterWms extension to load the AGS wms layer
    agsMap.map.lyrs.agsindex = L.tileLayer.wms('https://map.bgs.ac.uk/arcgis/services/AGS/AGS_Export/MapServer/WMSServer?', {
        layers: 'Boreholes',
        format: 'image/png',
        transparent: true,
        attribution: "AGS Data from British Geological Survey",
        zIndex: 1001
    }).addTo(agsMap.map.lMap);

    // Use the Leaflet.FeatureGroup.OGCAPI.js extension to load the AGS OGCAPI-Features layer
    agsMap.map.lyrs.agsboreholes = L.featureGroup.ogcApi("https://ogcapi.bgs.ac.uk/",{
        "collection":"agsboreholeindex",
        "pane":"overlays",
        "limit":200,
        "onEachFeature": function (feat, layer) {
            var properties = feat.properties;
            var popupContent = "<b>AGS Borehole Information</b><br><hr>" +
                "<b>BGS LOCA ID: </b>" + properties.bgs_loca_id + "<br>" +
                "<b>Depth (m): </b>" + properties.loca_fdep + "<br>" +
                "<b>Project Name: </b>" + properties.proj_name + "<br>" +
                "<b>Project Engineer: </b>" + properties.proj_eng + "<br>" +
                "<b>Project Contractor: </b>" + properties.proj_cont + "<br>" +
                "<b>Original LOCA ID: </b>" + properties.loca_id + "<br>" +
                "<b>AGS Graphical Log: </b>" + "<a href=" + "https://agsapi.bgs.ac.uk/ags_log/?bgs_loca_id=" + properties.bgs_loca_id + " target=" + "_blank" + ">View</a> / " +"<a href=" + "https://agsapi.bgs.ac.uk/ags_log/?bgs_loca_id=" + properties.bgs_loca_id + "&response_type=attachment" + ">Download</a>" + "<br>" +
                "<b>AGS Data (NGDC Download Service): </b>" + "<a href=" + "/ags_export/?bgs_loca_id=" + properties.bgs_loca_id + " target=" + "_blank" + ">Download</a>" + "<br>" +
                "<b>AGS Submission Record (raw data): </b>" + "<a href=" + properties.dad_item_url + " target=" + "_blank" + ">View</a>" + "<br>";
            layer.bindPopup(popupContent);
            },
        });
    agsMap.map.lyrs.agsboreholes.on("ready", () => {agsMap.map.lMap.addLayer(agsMap.map.lyrs.agsboreholes);})

    // add layer selection control
    overlays["<span>Geology</span>"]=agsMap.map.lyrs.geologyOfbtn;
    baseLayers["<span>Topographic</span>"]=agsMap.map.basemaps.topo;
    baseLayers["<span>Imagery</span>"]=agsMap.map.basemaps.imagery;
    agsMap.map.control=L.control.layers(baseLayers,overlays,{"collapsed":false}).addTo(agsMap.map.lMap);

    // add placeholder layer for drawings
    agsMap.map.lyrs["drawings"]=L.featureGroup().addTo(agsMap.map.lMap);

    // add placeholder layer for map highlight
    agsMap.map.lyrs["highlight"]=L.layerGroup().addTo(agsMap.map.lMap);

    // add drawing control
    agsMap.drawing.addControl();

    return true;
    };

// DRAWING ============================================================ DRAWING

agsMap.drawing={};
agsMap.drawing.shapes={"rectangle":true,"circle":false,"polyline":false,"polygon":true,"circlemarker":false,"marker":false};
agsMap.drawing.drawCtrlActive=false;
agsMap.drawing.showWMSpopup=true;

agsMap.drawing.reEnableWMSpopup=function(){
    console.log("reEnableWMSpopup");
    agsMap.drawing.showWMSpopup=true;
    return true;
    };

agsMap.drawing.addControl=function(){
    console.log("agsMap.drawing.addControl");

    // create drawing control
    agsMap.map.drawCtrl=new L.Control.Draw({
        "draw":agsMap.drawing.shapes,
        "edit":{"featureGroup":agsMap.map.lyrs.drawings}
        });
    agsMap.map.lMap.addControl(agsMap.map.drawCtrl);
    agsMap.drawing.drawCtrlActive=true;

    // add drawing DRAWSTART event
    agsMap.map.lMap.on(L.Draw.Event.DRAWSTART, function(evt){
        // prevent WMS popup while drawing
        agsMap.drawing.showWMSpopup=false;
        });
    agsMap.map.lMap.on(L.Draw.Event.DRAWSTOP, function(evt){
        // enable WMS popup after short delay to allow rectangle end point to be blocked
        window.setTimeout(agsMap.drawing.reEnableWMSpopup,1000);
        });

    // add drawing CREATED event
    agsMap.map.lMap.on(L.Draw.Event.CREATED, function(evt){
        var layer=evt.layer;
        var polyData=agsMap.drawing.getPolygonData(layer);
        var xhtml="Area: " + polyData.area + "<br /><input type='button' value='check for boreholes' class='checkPolyBtn' />";
        agsMap.polyData=polyData;
        agsMap.showExtentModal(polyData);
        agsMap.map.lyrs.drawings.addLayer(layer);
        // disable drawing - only one box allowed
        agsMap.drawing.disableDrawing();
        layer.bindPopup(xhtml);
        });

    // add drawing DELETESTOP event
    agsMap.map.lMap.on(L.Draw.Event.DELETESTOP, function(evt){
        agsMap.drawing.enableDrawing();
        });

    // add drawing EDITSTART event
    agsMap.map.lMap.on(L.Draw.Event.EDITSTART, function(evt){
        agsMap.map.lMap.closePopup();
        });

    // add drawing EDITED event
    agsMap.map.lMap.on(L.Draw.Event.EDITED, function(evt){
        var layerId=Object.getOwnPropertyNames(evt.layers._layers)[0];
        var layer=evt.layers._layers[layerId];
        var polyData=agsMap.drawing.getPolygonData(layer);
        var xhtml="Area: " + polyData.area + "<br /><input type='button' value='check for boreholes' class='checkPolyBtn' />";
        agsMap.polyData=polyData;
        agsMap.showExtentModal(polyData);
        layer.bindPopup(xhtml);
        });
    return true;
    };

agsMap.drawing.getPolygonData=function(layer){
    var polyData={"wkt":"","area":""};
    var coords=layer._latlngs[0];
    var wktPt="";
    var wktPts=[];
    var i=0;
    // calculate polygon area
    polyData.area=agsMap.calcPolygonArea(coords);
    // generate WKT
    for(i=0;i < layer._latlngs[0].length;i++){
        wktPt=layer._latlngs[0][i].lng.toFixed(3) + "%20" + layer._latlngs[0][i].lat.toFixed(3);
        wktPts.push(wktPt);
        };
    // add first point again to close WKT polygon
    wktPt=layer._latlngs[0][0].lng.toFixed(3) + "%20" + layer._latlngs[0][0].lat.toFixed(3);
    wktPts.push(wktPt);
    polyData.wkt="POLYGON((" + wktPts.join(",") + "))";
    return polyData;
    };

// --- toggle drawing mode ----------------------------------------------------

agsMap.drawing.disableDrawing=function(){
    var shapes={"rectangle":false,"circle":false,"polyline":false,"polygon":false,"circlemarker":false,"marker":false};
    agsMap.map.lMap.removeControl(agsMap.map.drawCtrl);
    agsMap.map.drawCtrl=new L.Control.Draw({
        "draw":shapes,
        "edit":{"featureGroup":agsMap.map.lyrs.drawings}}
        );
    agsMap.map.lMap.addControl(agsMap.map.drawCtrl);
    agsMap.drawing.drawCtrlActive=false;
    return true;
    };

agsMap.drawing.enableDrawing=function(){
    agsMap.map.lMap.removeControl(agsMap.map.drawCtrl);
    agsMap.map.drawCtrl=new L.Control.Draw({
        "draw":agsMap.drawing.shapes,
        "edit":{"featureGroup":agsMap.map.lyrs.drawings}}
        );
    agsMap.map.lMap.addControl(agsMap.map.drawCtrl);
    agsMap.drawing.drawCtrlActive=true;
    return true;
    };

agsMap.showExtentModal=function(polyData){
    $("#polyArea").html(polyData.area);
    $("#polyCount").html("(loading ...)");
    $("#extentModal>p.extentMsg").hide();
    $("#extentValid>a").attr("href","#");
    agsMap.checkExtent(polyData.wkt);
    agsMap.positionExtentModal();
    $("#extentModal").show();
    return true;
    };

agsMap.positionExtentModal=function(){
    var mapOffset=$("#mapid").offset();
    var mapWidth=$("#mapid").width();
    $("#extentModal").css("width",mapWidth + "px").css("left",mapOffset.left + "px").css("top",mapOffset.top + "px");
    return true;
    };

// AREA CALCULATION ===========================================================
agsMap.calcPolygonArea=function(coords){
    var area=L.GeometryUtil.readableArea(L.GeometryUtil.geodesicArea(coords),true);
    return area;
    };

agsMap.checkPoly=function(evt){
    agsMap.map.lMap.closePopup();
    agsMap.showExtentModal(agsMap.polyData);
    return true;
    };

// CHECK HOW MANY BOREHOLES IN EXTENT =========================================
agsMap.checkExtent=function(wkt){
    var apiUrl="/ags_export_by_polygon/?polygon=" + wkt + "&count_only=True";

    // UNCOMMENT LINE BELOW
    $.getJSON(apiUrl,agsMap.parseExtent);

    // DELETE TWO LINES BELOW
    //var fakeData={"msg":"Borehole count","count":7,"type":"success","self":"http://agsapi.bgs.ac.uk/ags_export_by_polygon/?polygon=POLYGON((-2.813%2055.317,-2.813%2055.466,-2.527%2055.466,-2.527%2055.317,-2.813%2055.317))&count_only=True"};
    //agsMap.parseExtent(fakeData);

    return true;
    };

agsMap.parseExtent=function(jData){
    var apiUrl=jData.self.replace("&count_only=True","");
    if(jData.type === "success"){
        if(jData.count === 0){
            // no bores
            $("#boreCount").html("none found");
            $("#extentEmpty").show();
            }
        else{
            if(jData.count <= agsMap.maxBoresForDownload){
                // got bores
                $("#boreCount").html(jData.count);
                $("#extentValid>a").attr("href",apiUrl);
                $("#extentValid").show();
                }
            else{
                // too many bores
                $("#boreCount").html(jData.count);
                $("#extentOver").show();
                };
            };
        }
    else{
        // error
        $("#boreCount").html("error");
        $("#extentEmpty").show();
        };
    return true;
    };

// FIRE INITIALISATION onDomReady =============================================
$(document).ready(agsMap.init);
