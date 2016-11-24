// $(window).load(function() {
// 	$('#sidebar').stick_in_parent();
// });

$( document ).ready(function() {
	$(window).on('resize', Foundation.utils.throttle(function(e){
		fill_hero();
		if (Foundation.utils.is_small_only()){
			search_form_open();
			$('.topbar_continer').removeClass('contain-to-grid');


		} else {
			search_form_close();
			$('.topbar_continer').addClass('contain-to-grid')
		}
	}, 300));

	$( window ).resize(function() {
	  if ( $( "#sidebar" ).length ) {
	  	set_Sidebar_width();	
	  }  
	});

// Temporarily disabled: see #369 and #408
//	ouibounce(false, {
//	       callback: function() {
//	           $('#newsletter_signup').foundation('reveal', 'open');
//	       }
//	 });

	function fill_hero(){
		var max_height = 620;
		var w_height = $(window).height();
		if (w_height < max_height) {
			var hero_h = w_height - 120;
			$('.hero_wraper').height (hero_h);
		} else {
			var hero_h = max_height;
			$('.hero_wraper').height (hero_h);
		}
	};

	if (window.location.pathname != '/') {
		var mascot_src = ["/img/mascot_1.png", "/img/mascot_2.png","/img/mascot_3.png"]
		var randon_mascot = Math.floor(Math.random() * mascot_src.length) + 1  
		$("#footer_mascot").attr('src', mascot_src[randon_mascot]);
	}

	// style h4 in kb
	$('#content h4').last().css( "margin-bottom", "1rem" );

	// show promo
	setTimeout(showPromo, 3000);

	$('.close_promo').click(function(e) {
		e.preventDefault();
		$('#promo').addClass("off")
	})

	function showPromo(){
		$('#promo').removeClass("off");
	}

	//sticky sidebar
	var scrollTop;
	var elementOffset;
	var distance;
	var footer_dist;
	var footer_offset;
	var el = $('#sidebar');
	var el_inner = $("#sidebar .side-nav")
	var footer = $("#footer")

	function set_Sidebar_width (){
		var w = Math.floor($('#sidebar').parent().width() * 0.25);
		el_inner.width(w);
	}

	set_Sidebar_width();

	$( window ).scroll(function() {
		if ( $( "#sidebar" ).length ) {
		  scrollTop     = $(window).scrollTop();
	      elementOffset = el.offset().top;
	      footer_offset	= footer.offset().top;
	      distance      = (elementOffset - scrollTop);

	      footer_dist	= scrollTop + el_inner.height();

	      if (distance < 0 && footer_dist < footer_offset ) {
	      	
	      	$('#sidebar .side-nav').addClass("stick");
	      } else {
	      	$('#sidebar .side-nav').removeClass("stick");
	      }
		}
	});




	// Search form View
	$('.search_icon').click (search_form_open);
	function search_form_open (){
		$('.search_icon').addClass("hide");
		$('.search_continer').removeClass ("hide");
	}

	function search_form_close (){
		$('.search_icon').removeClass("hide");
		$('.search_continer').addClass ("hide");
	}

	fill_hero();
	$(window).resize(fill_hero);

	//HP feture list
	$('.features_list').slick({
	  dots: true,
	  infinite: false,
	  speed: 300,
	  prevArrow: '<a class="icon-arow_left arow prevArrow animated"></a>',
	  nextArrow: '<a class="icon-arow_right arow nextArrow animated"></a>',
	  slidesToShow: 4,
	  slidesToScroll: 4,
	  responsive: [
	    {
	      breakpoint: 1024,
	      settings: {
	        slidesToShow: 4,
	        slidesToScroll: 4,
	        infinite: true,
	        dots: true
	      }
	    },
	    {
	      breakpoint: 600,
	      settings: {
	        slidesToShow: 2,
	        slidesToScroll: 2,
	        arrows: false,
	        dots: true
	      }
	    },
	    {
	      breakpoint: 480,
	      settings: {
	        slidesToShow: 1,
	        slidesToScroll: 1,
	        arrows: false,
	        dots: true
	      }
	    }
	    // You can unslick at a given breakpoint now by adding:
	    // settings: "unslick"
	    // instead of a settings object
	  ]
	});

	var tps_slider = $('.tps_list').slick({
		autoplay: true,
		autoplaySpeed: 6000,
		prevArrow: '<a class="icon-arow_left arow prevArrow animated"></a>',
		nextArrow: '<a class="icon-arow_right arow nextArrow animated"></a>',
		infinite: false,
		arrows: true,
		responsive: [
		{
		  breakpoint: 600,
		  settings: {
		  	dots: true
		  }
		}
		// You can unslick at a given breakpoint now by adding:
		// settings: "unslick"
		// instead of a settings object
		]
	});

	tps_slider.on('beforeChange', function(event, slick, currentSlide, nextSlide){
		if (Foundation.utils.is_medium_up()){
			nextSlide = nextSlide +1
			$('ul.tps_nav > li').removeClass("tps_nav_curent");
			var curent_tab = $('ul.tps_nav > li:nth-child(' + nextSlide + ')');
			curent_tab.addClass("tps_nav_curent");
			var x = curent_tab.offset();
			$('.marker').offset({left: x.left});
		}
	});

	$('.tps_nav_item').click(function(e) {
	    var slideIndex = $(this).closest('li').index();
	    tps_slider.slick( 'slickGoTo', parseInt( slideIndex ) ); 
	    var x = $(this).offset();
	    $('.marker').offset({left: x.left});
	    e.preventDefault();
	});

	tps_slider.slick( 'slickGoTo', parseInt( 0 ) );

	// handle sideBar

	//$('.side-nav li:has("ul")').children('ul').addClass('hide'); //hide submenu
	$('.side-nav li:has("ul")').addClass('hasChildren'); // add class to li ul child
	$('.side-nav li:has("ul") > a').click(function(){
	$(this).parent().toggleClass( "active_nav_item" ) // add active class to clicked menu item
	    $(this).parent().find('ul').toggleClass('hide'); //toggle submenu
	});

	if ( $( ".events_list" ).length ) {
		$('.events_list').slick({
		  autoplay: true,
		  autoplaySpeed: 10000,
		  vertical: true
		});
	}


	//chart setup

	if ( $( ".ct-chart" ).length ) {
		var options = {
		  seriesBarDistance: 22,
		  chartPadding: {
		      top: 15,
		      right: 15,
		      bottom: 25,
		      left: 20
		    },
		    axisY: {
		    	labelInterpolationFnc: function(value) {
	    	      return (value / 1000) + 'k';
	    	    }
		      },
		    plugins: [
		        Chartist.plugins.ctAxisTitle({
		          axisX: {
		            axisTitle: '',
		            axisClass: 'ct-axis-title',
		            offset: {
		              x: 0,
		              y: 0
		            },
		            textAnchor: 'middle'
		          },
		          axisY: {
		            axisTitle: 'Transaction/sec',
		            axisClass: 'ct-axis-title',
		            offset: {
		              x: 0,
		              y: -80
		            },
		            textAnchor: 'middle',
		            flipTitle: false
		          }
		        })
		      ]
		};

		var responsiveOptions = [
		  ['screen and (max-width: 640px)', {
		    seriesBarDistance: 12,
		    barWidth: 7,
		    chartPadding: {
		        top: 15,
		        right: 0,
		        bottom: 0,
		        left: 0
		      }
		  }]
		];

		new Chartist.Bar('.ct-chart', scylla_vs_cassandra_data, options, responsiveOptions);

		var $chart = $('.ct-chart');

		var $toolTip = $chart
		  .append('<div class="tooltip"></div>')
		  .find('.tooltip')
		  .hide();

		$chart.on('mouseenter', '.ct-bar', function() {
		  var $point = $(this),
		    value = $point.attr('ct:value'),
		    seriesName = $point.parent().attr('ct:series-name');
		  $toolTip.html(seriesName + '<br>' + value).show();
		  $toolTip.css({
		    left: ($point.attr('x1')) - $toolTip.width() / 2 - 20,
		    top: ($point.attr('y2')) - $toolTip.height() - 40
		  });

		});

		

		$chart.on('mouseleave', '.ct-bar', Foundation.utils.debounce(function(e){
		  $toolTip.hide();
		}, 3000, true));
	}
});
