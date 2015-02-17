$(document).ready(function() {
	// From https://gist.github.com/alanhamlett/6316427
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE' || settings.type == 'PATCH') {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		}
	});

	// Toggle synopses
	$("a.toggle-synopses").on("click", function() {
		$("#outline-panel").toggleClass("show-synopses");
		return false;
	});

	// Autosize
	$('#scene-panel textarea').autosize();


	// Textarea focus
	$("textarea#text").on("focus", function() {
		$("body").addClass("dimmer");
	});

	$("textarea#text").on("blur", function() {
		$("body").removeClass("dimmer");
	});


	// Reordering scenes in the outline
	$("#scene-list").sortable({
		placeholder: "scene placeholder",
		update: function(event, ui) {
			var order = {};
			var items = ui.item.parents("#scene-list:first").find("a.scene");

			for (var i=0; i<items.length; i++) {
				var item = $(items[i]);
				order[item.attr("data-id")] = i + 1;
			}

			var storySlug = $("#main").attr("data-story-slug");
			var url = '/api/story/' + storySlug + '/reorder-scenes/';

			$.ajax({
				url: url,
				method: 'POST',
				contentType: 'application/json',
				data: JSON.stringify({ "order": order }),
				success: function(data) {
					// Reorder scene numbers
					for (var i in order) {
						$("#scene-list a[data-id=" + i + "] span").html(order[i]);
					}
				},
				error: function(data) {
					console.log("Error! :(", data);
				},
			});
		},
	});
});

// From https://gist.github.com/alanhamlett/6316427
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i=0; i<cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
