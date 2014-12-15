$(document).ready(function() {
	$('.thumb-img').each(function() {
		var img = $(this);
		var width = img.width();
		var height = img.height();

		if (width > height) {
			img.width(200);
		} else {
			img.height(200);
			height = 200;
		}

		img.css({"top":"50%","margin-top":-height/2 + "px"});
	});

	$('.alert-hider').each(function() {
		$(this).delay(2000).fadeOut();
	});
});