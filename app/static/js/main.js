// main.2.js

var bgsMain={};

bgsMain.timerId=-1;
bgsMain.timerMs=500;

bgsMain.longTimerId=-1;
bgsMain.longTimerMs=10000;

bgsMain.init=function(){
    $("nav").css("opacity","0");
    bgsMain.resizePage();
    bgsMain.setCopyrightYear();
    bgsMain.setupNav();
    bgsMain.setupMobileMenu();
    bgsMain.setupPage();
    bgsMain.setupEvents();
    return true;
    };

bgsMain.setupPage=function(){
    $("nav").hide();
    $("nav>ul.level3").hide();
    $("#level2>li").hide();
    return true;
    };

bgsMain.setupEvents=function(){
    // RESIZE
    $(window).on("resize",bgsMain.resize);
    // MENU level 1 : over
    $("header").on("mouseenter","article.nav>p>a",bgsMain.menu1over);
    // MENU level 2 : over
    $("#level2").on("mouseenter","li>ul>li",bgsMain.menu2over);
    // MENU close
    $("nav").on("mouseleave",bgsMain.navout);
    // MENUBARS (hamburger) click
    $("header").on("click","img.menubars",bgsMain.menubarsClick);
    // MOBILE MENU click
    $("#mobileMenu").on("click","li",bgsMain.mobileMenuClick);
    return true;
    };

bgsMain.resize=function(evt){
    bgsMain.resizePage();
    return true;
    };

bgsMain.menu1over=function(evt){
    var a=$(evt.target).closest("a");
    bgsMain.showNav2(a);
    return true;
    };

bgsMain.menu2over=function(evt){
    var li=$(evt.target).closest("li");
    bgsMain.showNav3(li);
    return true;
    };

bgsMain.navout=function(evt){
    // add slight delay for mouse transition
    if(bgsMain.timerId !== -1){
        window.clearTimeout(bgsMain.timerId);
        bgsMain.timerId=-1;
        };
    bgsMain.timerId=window.setTimeout(bgsMain.hideNav,bgsMain.timerMs);
    return true;
    };

bgsMain.menubarsClick=function(evt){
    var img=$(evt.target);
    $("nav").hide();
    if(img.hasClass("open")){
        // close menus
        img.attr("src","//resources.bgs.ac.uk/webapps/resources/images/menu-bars.svg").removeClass("open");
        $("header>section.topnav").show();
        $("header>section.breadcrumbs").show();
        $("main").show();
        $("footer").show();
        $("#mobileMenu").hide();
        }
    else{
        // open menus
        img.attr("src","//resources.bgs.ac.uk/webapps/resources/images/menu-close.svg").addClass("open");
        $("header>section.topnav").hide();
        $("header>section.breadcrumbs").hide();
        $("main").hide();
        $("footer").hide();
        $("#mobileMenu").show();
        };
    return true;
    };

bgsMain.mobileMenuClick=function(evt){
    var li=$(evt.target).closest("li");
    var ul=li.closest("ul");
    evt.stopPropagation();
    // top
    if(li.hasClass("mm_lvl_1")){
        if(li.hasClass("open")){
            li.removeClass("open");
            $("#mobileMenu>ul>li").show();
            }
        else{
            $("#mobileMenu ul.mm_lvl_1>li").removeClass("open");
            $("#mobileMenu>ul>li").hide();
            li.addClass("open").show();
            };
        }
    else{
        // middle
        if(li.hasClass("mm_lvl_2") && li.hasClass("expands")){
            if(li.hasClass("open")){
                $("#mobileMenu ul.mm_lvl_2 li").show();
                $("#mobileMenu>ul>li>strong").show();
                $("#mobileMenu>ul>li>em").show();
                li.removeClass("open");
                }
            else{
                $("#mobileMenu ul.mm_lvl_2>li").hide();
                $("#mobileMenu>ul>li>strong").hide();
                $("#mobileMenu>ul>li>em").hide();
                li.addClass("open").show();
                };
            };
        };
    return true;
    };

// ===============

bgsMain.setupMobileMenu=function(){
    var topLevels=["About","Research","Data","DiscoGeo"];
    var i=0;
    var p1={};
    var a1={};
    var li2s={};
    var xhtml="";
    console.log("bgsMain.setupMobileMenu");

    xhtml=xhtml + "<ul class='mm_lvl_1'>";
    for(i=0;i < topLevels.length;i++){
        p1=$("header>section.logonav>article.nav>p." + topLevels[i]);
        a1=p1.children("a");
        li2s=$("#ul" + topLevels[i] + ">ul>li");

        xhtml=xhtml + "<li class='mm_lvl_1'>";

            xhtml=xhtml + "<strong>" + a1.text() + "</strong> <em>&nbsp;</em>";

            xhtml=xhtml + "<ul class='mm_lvl_2'>";
            li2s.each(function(){
                var a2=$(this).children("a");
                var em2=$(this).children("em");
                var ul3id="";
                var li3s={};
                var j=0;
                if($(this).children("em").length === 1){
                    ul3id="ul" + topLevels[i] + "_" + a2.attr("href").split("/").reverse()[1];
                    li3s=$("#" + ul3id + ">li");
                    xhtml=xhtml + "<li class='mm_lvl_2 expands'>";
                    xhtml=xhtml + "<a href='" + a2.attr("href") + "'>" + a2.text() + "</a> <em>&nbsp;</em>";
                    xhtml=xhtml + "<ul class='mm_lvl_3'>";
                        li3s.each(function(){
                            var a3=$(this).children("a");
                            xhtml=xhtml + "<li class='mm_lvl_3'><a href='" + a3.attr("href") + "'>" + a3.text() + "</a></li>";
                            });
                    xhtml=xhtml + "</ul>";
                    xhtml=xhtml + "</li>";
                    }
                else{
                    xhtml=xhtml + "<li class='mm_lvl_2'><a href='" + a2.attr("href") + "'>" + a2.text() + "</a></li>";
                    }

                });
            xhtml=xhtml + "</ul>";

        xhtml=xhtml + "</li>";
        };

    xhtml=xhtml + "</ul>";

    $("#mobileMenu").html(xhtml).hide();
    return true;
    };

// ===================================================

bgsMain.resizePage=function(){
    var img=$("header section.logonav article.nav img.menubars");
    var w=$(window).width();
    var bodyClass="width1";
    var currClass=$("body").attr("class");
    if(w > 576){
        bodyClass="width2";
        if(w > 768){
            bodyClass="width3";
            if(w > 992){
                bodyClass="width4";
                if(w > 1200){
                    bodyClass="width5";
                    };
                };
            };
        };
    if(bodyClass !== currClass){
            $("body").attr("class",bodyClass);
            // close mobileMenu if open
            if(img.hasClass("open")){img.click();};
            };
    return true;
    };


bgsMain.setupNav=function(){
    var li2=$("#level2");
    var li3s=li2.children("li");
    li3s.each(function(){
        var li3=$(this);
        var li3Ht=(li3.find("ul>li").length * 40) - 10;
        $("nav>ul[rel='" + li3.attr("id") + "']").css("height",li3Ht + "px");
        });
    return true;
    };

bgsMain.hideNav=function(){
    $("header>section.logonav>article.nav>p>a").removeClass("open");
    $("nav>ul>li>ul>li").removeClass("open");
    $("nav>ul.level3").hide();
    $("nav").hide();
    return true;
    };

bgsMain.showNav2=function(a){
    $("nav").css("opacity","1.0");
    var code=a.attr("href").substring(1);
    // cancel hide timer
    if(bgsMain.timerId !== -1){
        window.clearTimeout(bgsMain.timerId);
        bgsMain.timerId=-1;
        };
    $("nav>ul.level3").hide();
    $("header>section.logonav>article.nav>p>a").removeClass("open");
    a.addClass("open");
    $("#level2>li").hide();
    $("#ul" + code).show();
    if($("nav").is(":visible")){$("nav").show();}
    else{$("nav").slideDown();};
    bgsMain.startLongTimer();
    return true;
    };

bgsMain.showNav3=function(li){
    $("nav").css("opacity","1.0");
    var a=li.children("a");
    var urlArr=a.attr("href").split("/");
    var parentLi=li.closest("ul").closest("li");
    var childCode=parentLi.attr("id") + "_" + urlArr[urlArr.length - 2];
    var childUl=$("#" + childCode);
    $("nav>ul>li>ul>li").removeClass("open");
    li.addClass("open");
    $("nav>ul.level3").hide();
    $("nav>ul.level3>li.empty").show();
    if(childUl.length > 0){childUl.show();};
    bgsMain.startLongTimer();
    return true;
    };

bgsMain.setCopyrightYear=function(){
    var cyYear=new Date().getFullYear();
    var cyText=document.createTextNode(cyYear.toString());
    var cyElem=document.getElementById("copyrightYear");
    cyElem.removeChild(cyElem.firstChild);
    cyElem.appendChild(cyText);
    return true;
    };

bgsMain.startLongTimer=function(){
    // add long delay to clear meneus after inactivity
    console.log("startLongTimer");
    if(bgsMain.longTimerId !== -1){
        window.clearTimeout(bgsMain.longTimerId);
        bgsMain.longTimerId=-1;
        };
    bgsMain.longTimerId=window.setTimeout(bgsMain.hideNav,bgsMain.longTimerMs);
    return true;
    };

// ===================================================

window.onload=function(){
    bgsMain.init();
    };