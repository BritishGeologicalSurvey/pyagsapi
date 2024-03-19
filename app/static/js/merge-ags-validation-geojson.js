// merge-ags-validation-geojson.js
var mavg={};

mavg.downloadData={"type":"FeatureCollection","features":[]};

mavg.mergeGeoJSON=function(agsValidationResult){
    var i=0;
    var j=0;
    var fileRes={};
    var feature={};
    // reset downloadData to remove any previous results
    mavg.downloadData.features=[];
    // loop file(s)
    for(i=0;i < agsValidationResult.data.length;i++){
        fileRes=agsValidationResult.data[i];
        // loop features - add filename to feature properties - append to downloadData
        if(!fileRes.geojson_error && fileRes.geojson && fileRes.geojson.features && fileRes.geojson.features.length > 0){
            for(j=0;j < fileRes.geojson.features.length;j++){
                feature=fileRes.geojson.features[j];
                feature.properties.filename=fileRes.filename;
                mavg.downloadData.features.push(feature);
                };
            };
        };
    return true;
    };

mavg.downloadMergedGeoJSON=function(){
    var ts=new Date().toISOString().substr(0,10);
    var fileName="";
    var fileText="";
    var dlLink={};
    // check we have some data to download
    if(mavg.downloadData.features.length > 0){
        // create <a> element and use data-url to download GeoJSON
        fileName="BGS-AGS-Validation-GeoJSON-" + ts + ".json";
        fileText=JSON.stringify(mavg.downloadData);
        dlLink=document.createElement('a');
        dlLink.href='data:application/geo+json;charset=utf-8,' + encodeURI(fileText);
        dlLink.target='_blank';
        dlLink.download=fileName;
        dlLink.click();
        };
    return true;
    };
