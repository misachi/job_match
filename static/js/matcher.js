$(document).ready(function(){
		$(".auto_animate").fadeIn(1000);

		$(".nav-tabs a:first").tab("show");

		$(".brand").addClass("animated");

		var window_width = $(window).width();

		if (window_width <= 1500) {

			 $("#padding-top").addClass("padding-top-10");

		}
//		$('#new_field').on("click", function () {
//            $('#add').append('
//
//            ')
//        })
});