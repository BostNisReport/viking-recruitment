// @codekit-prepend "jquery.carouFredSel-6.2.1.js";
// @codekit-prepend "transition.js";
// @codekit-prepend "carousel.js";


/* global $ */

$().ready(function() {
    "use strict";

    var homepage_carousel = $("#homepage_carousel"),
        menu = $("#primary_nav");

        homepage_carousel.carousel({
            interval: 3000
        });
        homepage_carousel.find(".pause").on("click", function(event) {
            event.preventDefault();
            homepage_carousel.carousel("pause");
        });

        $("#course_availability").carousel({
            interval: 0
    });

    $("#toggle-pulldown").on("click", function(event) {
        event.preventDefault();
        $("#pulldown").toggle("fast");
    }).css("visibility", "visible");

    $("#menutoggle").on("click", function(event) {
        event.preventDefault();
        var primary_nav = $(".brand #primary_nav");
        primary_nav.toggle("fast").toggleClass('menu-open');
        if (!(primary_nav.hasClass('menu-open'))) {
            menu_groups.hide(0);
        }
    });

    $("a").each(function() {
        var a = new RegExp("/" + window.location.host + "/");
        if(!a.test(this.href)) {
            $(this).click(function(event) {
                event.preventDefault();
                event.stopPropagation();
                window.open(this.href, "_blank");
            });
        }
    });

    var megamenu = $("#megamenu"),
        menu_groups = megamenu.find(".megamenu_group"),
        active_group = megamenu.find(".megamenu_group_active"),
        primary_nav = $("#primary_nav"),
        primary_active = primary_nav.find(".default_active");

    primary_nav.on("mouseenter", "a", function() {
        var menu_group = $(this).data("megamenugroup");
        primary_nav.find(".active").removeClass("active");
        $(this).addClass("active");
        menu_groups.hide(0);
        $("#megamenu_group_" + menu_group).show(0);
    });
    $("#meganav").on("mouseleave", function() {
        primary_nav.find(".active").removeClass("active");
        primary_active.addClass("active");
        menu_groups.hide(0);
        active_group.show(0);
    });

    primary_nav.on("click", ".menu-option-toggle", function(e) {
        e.preventDefault();
        e.stopPropagation();
        var menu_group = $(this).parent().data("megamenugroup");
        var current_active = primary_nav.find(".mobile-active");
        current_active.removeClass("mobile-active");
        $(this).parent().addClass("mobile-active");
        menu_groups.hide(0);
        $("#megamenu_group_" + menu_group).show(0);
    });

    $("#latestjobs").carouFredSel({
        circular: true,
        infinite: true,
        auto: false,
        prev: {
            button: "#latestjobs_prev"
        },
        next: {
            button: "#latestjobs_next"
        },
        pagination: "#latestjobs_pips"
    }, {
        wrapper: "parent"
    });

    // Dropdown toggle
    $('.dropdown-families').click(function(){
        $(this).next('.dropdown').toggle();
    });

    // Registration
    $(".registration-form").on("submit", function() {
        var email = $(this).find("#id_email").val();
        var reversed_email = email.split("").reverse().join("");
        $(this).find("#id_anti_spam").val(reversed_email);
    });

    $(".apply-btn").on("click", function() {
        $(this).html("Applied");
    });
});
