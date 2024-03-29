$(".owl-carousel").owlCarousel({
  loop: true,
  margin: 10,
  autoplay: true,
  autoplayTimeout: 1000,
  autoplayHoverPause: false,
  responsive: {
    0: {
      items: 3,
    },
    300: {
      items: 4,
    },
    600: {
      items: 5,
    },
    1000: {
      items: 7,
    },
    1250: {
      items: 8,
    },
  },
});

document.addEventListener("DOMContentLoaded", function (event) {
  if ($(window).width() < 768) {
    $('.header_toggle').hide();
    $('.header_toggle_offcanvas').show();
  }else{
    $('.header_toggle').show();
    $('.header_toggle_offcanvas').hide();
  }
  if ($(window).width() < 480) {
    $('#navBarSearchForm').hide();
    $('.searchbarhidden').show();
  }else{
    $('#navBarSearchForm').show();
    $('.searchbarhidden').hide();
  }
  const showNavbar = (toggleId, navId, bodyId, headerId) => {
    const toggle = document.getElementById(toggleId),
      nav = document.getElementById(navId),
      bodypd = document.getElementById(bodyId),
      headerpd = document.getElementById(headerId);

    // Validate that all variables exist
    if (toggle && nav && bodypd && headerpd) {
      toggle.addEventListener("click", () => {
        // show navbar
        nav.classList.toggle("show");
        // change icon
        toggle.classList.toggle("bx-x");
        // add padding to body
        bodypd.classList.toggle("body-pd");
        // add padding to header
        headerpd.classList.toggle("body-pd");
      });
    }
  };

  showNavbar("header-toggle", "nav-bar", "body-pd", "header");

  /*===== LINK ACTIVE =====*/
  const linkColor = document.querySelectorAll(".nav_link");

  function colorLink() {
    if (linkColor) {
      linkColor.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");
    }
  }
  linkColor.forEach((l) => l.addEventListener("click", colorLink));

  // Your code to run since DOM is loaded and ready
});

$(window).resize(function () {
  if ($(this).width() < 768) {
    $(".header_toggle").hide();
    $(".header_toggle_offcanvas").show();
  } else {
    $('.header_toggle_offcanvas').hide();
    $(".header_toggle").show();
  }
});
$(window).resize(function () {
  if ($(this).width() < 480) {
    $('#navBarSearchForm').hide();
    $('.searchbarhidden').show();
  } else {
    $('#navBarSearchForm').show();
    $('.searchbarhidden').hide();
  }
});
