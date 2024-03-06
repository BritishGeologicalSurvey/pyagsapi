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
    xhtml=xhtml + '<div id="resultPopup">';
    xhtml=xhtml + '<h2>Validation results <input type="button" class="closeResPopopBtn" value="close" /></h2>';
    xhtml=xhtml + '<p id="res_Summary"></p>';
    // xhtml=xhtml + '<h2>Results for <span id="fileCount">-</span> file(s)</h2>';
    xhtml=xhtml + '<div id="res_Files"></div>';
    xhtml=xhtml + '</div>';
    $("#validator").after(xhtml);
    agsHtml.hideResultPopup();
    $("#validator input:submit").prop("disabled",true);
    $("#converter input:submit").prop("disabled",true);
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
    console.log("agsHtml.parseValidationError");
    console.log(xhr);
    alert("Sorry, there was an error calling the Validation API.");
    agsHtml.hideResultPopup();
    return true;
    };

agsHtml.parseValidationResponse=function(jData){
    var i=0;
    var fileResult={};
    $("#res_Summary").html(jData.msg);
    // $("#fileCount").html(jData.data.length);
    $("#res_Files").html("");
    for(i=0;i < jData.data.length;i++){
        fileResult=jData.data[i];
        agsHtml.displayFileResult(fileResult);
        };
    $("#resultPopup").show();
    if(agsMap && agsMap.positionExtentModal){agsMap.positionExtentModal();};
    return true;
    };

agsHtml.displayFileResult=function(fileResult){
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
    $("#res_Files").append(xhtml);
    return true;
    };

agsHtml.init=function(){
    agsHtml.injectEvents();
    agsHtml.injectHtmlOpt();
    agsHtml.injectResultPopup();
    return true;
    };

// FIRE INITIALISATION onDomReady =============================================
$(document).ready(agsHtml.init);
