// htmlView.js

var agsHtml={};

agsHtml.injectHtmlOpt=function(){
    var xhtml='<input type="radio" id="html" name="fmt" value="html" /><label for="html">HTML</label>';
    $("#validator>form>fieldset:eq(2)>legend").after(xhtml);
    $("#validator>form>fieldset:eq(2)>input:eq(2)").prop("checked",false);
    $("#validator>form>fieldset:eq(2)>input:eq(0)").prop("checked",true);
    return true;
    };

agsHtml.injectResultPopup=function(){
    var xhtml='';
    // generate HTML
    xhtml=xhtml + '<div id="resultPopup">';
    xhtml=xhtml + '<h2>Validation results <input type="button" class="closeResPopopBtn" value="close" /></h2>';
    xhtml=xhtml + '<p id="res_LoadMsg"><span class="rotate">&#x274D;</span> Validating file(s) ... please wait ...</p>';
    xhtml=xhtml + '<p id="res_Summary"></p>';
    xhtml=xhtml + '<div id="res_Files"></div>';
    xhtml=xhtml + '<div id="res_MapFrame"><div id="res_Map"></div></div>';
    xhtml=xhtml + '<p id="res_Download"><input type="button" id="downloadGeoJSONBtn" value="Download GeoJSON" disabled="disabled" /></p>';
    xhtml=xhtml + '</div>';
    // add to #validator section
    $("#validator").append(xhtml);
    // hide for now
    agsHtml.hideResultPopup();
    $("#validator input:submit").prop("disabled",true);
    $("#converter input:submit").prop("disabled",true);
    $("#downloadGeoJSONBtn").prop("disabled",true);
    // setup validation map
    agsHtml.setupValidationMap();
    return true;
    };

agsHtml.hideResultPopup=function(){
    $("#resultPopup").hide();
    if(agsMap && agsMap.positionExtentModal){agsMap.positionExtentModal();};
    return true;
    };

agsHtml.injectEvents=function(){
    $("#validateForm").on("submit",agsHtml.formSubmit);
    $("#validateForm").on("change","input:file",agsHtml.fileChange);
    $("#convertForm").on("change","input:file",agsHtml.convertFileChange);
    $("main").on("click","input.closeResPopopBtn",agsHtml.hideResultPopup);
    $("main").on("click","ul.fileResErrors>li",agsHtml.toggleErrorGroup);
    $("#identification").on("click","li",agsHtml.tabClick);
    $("main").on("click","#downloadGeoJSONBtn",agsHtml.downloadBtnClick);
    return true;
    };

agsHtml.downloadBtnClick=function(evt){
    // interface to fn in "merge-ags-validation-geojson.js"
    mavg.downloadMergedGeoJSON();
    return true;
    };

agsHtml.tabClick=function(evt){
    evt.preventDefault();
    var li=$(evt.target).closest("li");
    var a=li.children("a");
    if(!li.hasClass("open")){
        $("#identification>ul>li").removeClass("open");
        li.addClass("open");
        $("main>div.container>div.row>div>section.tabbed").hide();
        $(a.attr("href")).show();
        if(a.attr("href") === "#validator"){
            vMap.resetValidationMap();
            };
        };
    return true;
    };

agsHtml.checkFiles=function(fileList,extns){
    const maxFileSize=(50 * 1024 * 1024);
    const extnArr=extns.toLowerCase().split(",");
    var fileObj={};
    var fileExtn="";
    var fileCheck={"valid":true,"size":0,"errs":[]};
    if(fileList.length === 0){
        // no files selected
        fileCheck.valid=false;
        // fileCheck.errs.push("No files selected");
        fileCheck.errs=["No files"];
        }
    else{
        // loop selected files
        for(fileObj of fileList){
            fileCheck.size = fileCheck.size + fileObj.size;
            fileExtn=fileObj.name.split(".").reverse()[0].toLowerCase();
            if(!extnArr.includes(fileExtn)){
                fileCheck.valid=false;
                fileCheck.errs.push(fileObj.name + " is not of file type " + extnArr.join(" or ").toUpperCase() + "");
                };
            if(fileObj.size > maxFileSize){
                fileCheck.valid=false;
                fileCheck.errs.push(fileObj.name + " is larger than 50MB");
                };
            };
        // check overall size of file(s)
        if(fileCheck.size > maxFileSize){
            fileCheck.valid=false;
            fileCheck.errs.push("Total size of file(s) is larger than 50MB");
            };
        };
    return fileCheck;
    };

agsHtml.convertFileChange=function(evt){
    const currFiles=$("#convertForm input:file")[0].files;
    var fileCheck=agsHtml.checkFiles(currFiles,"xlsx,ags");
    if(fileCheck.valid){
        $("#convertForm input:submit").prop("disabled",false);
        }
    else{
        $("#convertForm input:submit").prop("disabled",true);
        alert(fileCheck.errs.join("\n"));
        };
    return true;
    };

agsHtml.fileChange=function(evt){
    const currFiles=$("#validateForm input:file")[0].files;
    // var fileCheck=agsHtml.checkFiles(currFiles,"ags,zip");
    var fileCheck=agsHtml.checkFiles(currFiles,"ags");
    if(fileCheck.valid){
        $("#validateForm input:submit").prop("disabled",false);
        }
    else{
        $("#validateForm input:submit").prop("disabled",true);
        alert(fileCheck.errs.join("\n"));
        };
    return true;
    };

agsHtml.toggleErrorGroup=function(evt){
    var li=$(evt.target).closest("li");
    li.children("ul").toggle();
    li.toggleClass("closed");
    return true;
    };

agsHtml.formSubmit=function(evt){
    var checkedRadios=$("#validator>form>fieldset:eq(2) input:checked");
    if(checkedRadios.length === 1){
        if(checkedRadios.val() === "html"){
            evt.preventDefault();
            $("#validator>form>fieldset:eq(2) input:submit").prop("disabled",true);
            // clear any previous validation results
            $("#res_Files").html("");
            $("#res_Summary").html("");
            $("#res_Download").hide();
            vMap.hideValidationMap();
            // submit form
            agsHtml.formSubmitForHTML();
            };
        }
    else{
        evt.preventDefault();
        alert("Select a format ...");
        };
    return true;
    };

agsHtml.formSubmitForHTML=function(){
    var apiUrl=$("#validator>form").attr("action");
    var formData=new FormData(document.getElementById("validateForm"));
    $("#res_LoadMsg").show();
    $("#resultPopup").show();
    formData.set("fmt","json");
    $.ajax({
        "type":"POST",
        "url":apiUrl,
        "data":formData,
        "processData":false,
        "contentType":false,
        "dataType":"json",
        "success":agsHtml.parseValidationResponse,
        "error":agsHtml.parseValidationError
        });
    return true;
    };

agsHtml.parseValidationError=function(xhr){
    // validation error
    console.log("agsHtml.parseValidationError");
    console.log(xhr);
    alert("Sorry, there was an error calling the Validation API.");
    agsHtml.hideResultPopup();
    return true;
    };

agsHtml.parseValidationResponse=function(jData){
    // validation success - show results
    console.log("agsHtml.parseValidationResponse");
    console.log(jData);
    var i=0;
    var fileResult={};
    $("#res_Summary").html(jData.msg);
    // clear any previous results
    $("#res_Files").html("");
    for(i=0;i < jData.data.length;i++){
        fileResult=jData.data[i];
        agsHtml.displayFileResult(fileResult,i);
        };
    $("#res_LoadMsg").hide();
    $("#res_Download").show();
    $("#resultPopup").show();
    if(agsMap && agsMap.positionExtentModal){agsMap.positionExtentModal();};
    return true;
    };

agsHtml.displayFileResult=function(fileResult,ix){
    console.log("agsHtml.displayFileResult");
    console.log(fileResult);
    console.log(ix);
    var xhtml="";
    var i=0;
    var errGroups=[];
    var errGroup="";
    var summaries=[];

    xhtml=xhtml + "<article>";

    if(fileResult.valid){xhtml=xhtml + "<h3 class='valid'><strong>" + fileResult.filename + "</strong> <em>" + fileResult.message + "</em></h3>";
        }
    else{
        xhtml=xhtml + "<h3 class='invalid'><strong>" + fileResult.filename + "</strong> <em>" + fileResult.message + "</em></h3>";
        };
    xhtml=xhtml + "<p><label>File Size</label> <strong>" + fileResult.filesize + " bytes</strong></p>";
    xhtml=xhtml + "<p><label>Checker(s)</label> <strong>" + fileResult.checkers.join(", ") + "</strong></p>";
    xhtml=xhtml + "<p><label>Dictionary</label> <strong>" + fileResult.dictionary + "</strong></p>";
    xhtml=xhtml + "<p><label>Time (UTC)</label> <strong>" + fileResult.time.substring(0,19).replace("T"," ") + "</strong></p>";

    if(fileResult.additional_metadata){

        summaries=Object.getOwnPropertyNames(fileResult.additional_metadata);

        xhtml=xhtml + "<h4>Summary</h4>";
        xhtml=xhtml + "<ul class='fileResSummary'>";

        if(summaries.length === 0){
            xhtml=xhtml + "<li>No summary generated due to errors reading file (see below) or BGS validation not selected (required for summary)</li>";
            };

        if(fileResult.additional_metadata.bgs_all_groups){
            xhtml=xhtml + "<li>" + fileResult.additional_metadata.bgs_all_groups + "</li>";
            };
        if(fileResult.additional_metadata.bgs_dict){
            xhtml=xhtml + "<li>" + fileResult.additional_metadata.bgs_dict + "</li>";
            };
        if(fileResult.additional_metadata.bgs_file){
            xhtml=xhtml + "<li>" + fileResult.additional_metadata.bgs_file + "</li>";
            };
        if(fileResult.additional_metadata.bgs_loca_rows){
            xhtml=xhtml + "<li>" + fileResult.additional_metadata.bgs_loca_rows + "</li>";
            };
        xhtml=xhtml + "</ul>";
        };

    errGroups=Object.getOwnPropertyNames(fileResult.errors).sort();
    if(errGroups.length > 0){
        xhtml=xhtml + "<h4>Errors</h4>";
        xhtml=xhtml + "<ul class='fileResErrors'>";
        for(i=0;i < errGroups.length;i++){
            errGroup=errGroups[i];
            groupErrs=fileResult.errors[errGroup];
            xhtml=xhtml + "<li>";
            xhtml=xhtml + "<strong>" + errGroup + "</strong> ";
            xhtml=xhtml + "<em>(&times;" + groupErrs.length + ")</em>";
            xhtml=xhtml + "<ul class='closed'>";
            for(j=0;j < groupErrs.length;j++){
                xhtml=xhtml + "<li>";
                if(groupErrs[j].line !== "-"){xhtml=xhtml + "<span>Line " + groupErrs[j].line + "</span> ";};
                xhtml=xhtml + groupErrs[j].desc.replace(/</g,"&lt;").replace(">","&gt;");
                xhtml=xhtml + "</li>";
                };
            xhtml=xhtml + "</ul></li>";
            };
        xhtml=xhtml + "</ul>";
        };
    xhtml=xhtml + "</article>";

    // clear any old data from validation map
    agsHtml.resetValidationMap();

    if(fileResult.geojson && fileResult.geojson.type){
        console.log("GOT GeoJSON");
        // show GeoJSON if returned + pass through filename for popup
        agsHtml.showOnValidationMap(fileResult.geojson,fileResult.filename,ix);
        // enable download button
        $("#downloadGeoJSONBtn").prop("disabled",false);
        }
    else{
        console.log("NO GeoJSON");
        // otherwise hide validation map + disable download button
        agsHtml.hideValidationMap();
        $("#downloadGeoJSONBtn").prop("disabled",true);
        };
    $("#res_Files").append(xhtml);
    return true;
    };

agsHtml.setupCollapsibles=function(){
    var coll = document.getElementsByClassName("collapsible");
    var i;
    for (i = 0; i < coll.length; i++){
        coll[i].addEventListener("click",function(){
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if(content.style.maxHeight){content.style.maxHeight = null;}
            else{content.style.maxHeight = content.scrollHeight + "px";}
        });
        };
    return true;
    };

// interfaces to vMap (validation-map.js)
agsHtml.setupValidationMap=function(){
    console.log("agsHtml.setupValidationMap");
    vMap.setupValidationMap();
    return true;
    };

agsHtml.showOnValidationMap=function(geoJSON,ix){
    console.log("agsHtml.showOnValidationMap");
    vMap.showOnValidationMap(geoJSON,ix);
    return true;
    };

agsHtml.resetValidationMap=function(){
    console.log("agsHtml.resetValidationMap");
    vMap.resetValidationMap();
    return true;
    };

agsHtml.hideValidationMap=function(){
    console.log("agsHtml.hideValidationMap");
    vMap.hideValidationMap();
    return true;
    };

// init
agsHtml.init=function(){
    agsHtml.injectEvents();
    agsHtml.injectHtmlOpt();
    agsHtml.injectResultPopup();
    agsHtml.setupCollapsibles();
    return true;
    };

// FIRE INITIALISATION onDomReady =============================================
$(document).ready(agsHtml.init);
