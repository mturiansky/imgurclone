$(document).ready(function() {
	$('.thumb-img').each(function() {
		var img = $(this);
		var width = img.width();
		var height = img.height();

		img.css({"top":"50%","margin-top":-height/2 + "px"});

		if (width > height) {
			img.width(200);
		} else {
			img.height(200);
		}
	});
});