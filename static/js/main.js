$(function() {

  var siteSticky = function() {
		$(".js-sticky-header").sticky({topSpacing:0});
	};
	siteSticky();

	var siteMenuClone = function() {

		$('.js-clone-nav').each(function() {
			var $this = $(this);
			$this.clone().attr('class', 'site-nav-wrap').appendTo('.site-mobile-menu-body');
		});


		setTimeout(function() {

			var counter = 0;
      $('.site-mobile-menu .has-children').each(function(){
        var $this = $(this);

        $this.prepend('<span class="arrow-collapse collapsed">');

        $this.find('.arrow-collapse').attr({
          'data-toggle' : 'collapse',
          'data-target' : '#collapseItem' + counter,
        });

        $this.find('> ul').attr({
          'class' : 'collapse',
          'id' : 'collapseItem' + counter,
        });

        counter++;

      });

    }, 1000);

		$('body').on('click', '.arrow-collapse', function(e) {
      var $this = $(this);
      if ( $this.closest('li').find('.collapse').hasClass('show') ) {
        $this.removeClass('active');
      } else {
        $this.addClass('active');
      }
      e.preventDefault();

    });

		$(window).resize(function() {
			var $this = $(this),
				w = $this.width();

			if ( w > 768 ) {
				if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
			}
		})

		$('body').on('click', '.js-menu-toggle', function(e) {
			var $this = $(this);
			e.preventDefault();

			if ( $('body').hasClass('offcanvas-menu') ) {
				$('body').removeClass('offcanvas-menu');
				$this.removeClass('active');
			} else {
				$('body').addClass('offcanvas-menu');
				$this.addClass('active');
			}
		})

		// click outisde offcanvas
		$(document).mouseup(function(e) {
	    var container = $(".site-mobile-menu");
	    if (!container.is(e.target) && container.has(e.target).length === 0) {
	      if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
	    }
		});
	};
	siteMenuClone();

});

// $(document).ready(function() {
//   $("#toggle").click(function() {
//     var elem = $("#toggle").text();
//       if (elem == "Read reviews") {
//         //Stuff to do when btn is in the read more state
//               $("#toggle").text("Done reading reviews?");
//               $("#text").slideDown();
//             } else {
//               //Stuff to do when btn is in the read less state
//             $("#toggle").text("Read reviews");
//         $("#text").slideUp();
//     }
// });
// });
//
// $(document).on('submit', '#commentForm', function(e){
// e.preventDefault();
// rates = $(document.getElementsByName('rate'));
// var rate_value;
// for(var i = 0; i < rates.length; i++){
// if(rates[i].checked){
//     rate_value = rates[i].value;
// }
// }
// $.ajax({
//   method:'POST',
//   url:"{% url 'product_detail' product.id %}",
//   data:{
//       rate:rate_value,
//       body:$('#id_body').val(),
//       csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//       action:'ajax-post'
//   },
//   success:function(json){
//       document.getElementById("commentForm").style.display = "none";
//       document.getElementById("success-display").style.display = "block";
//   },
//   error : function(xhr,errmsg,err) {
//   console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
// }
// });
// });
//
// $(document).on('submit', '#likeForm', function(e){
// e.preventDefault();
// $.ajax({
//   method:'POST',
//   url:"{% url 'like_product' product.pk %}",
//   data:{
//       product_id:$('#likeBtn').val(),
//       csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//       action:'ajax-post'
//   },
//   success:function(json){
//     console.log(json);
//     $("#wrapper div").replaceWith(json);
//   },
//   error : function(xhr,errmsg,err) {
//   console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
// }
// });
// });
