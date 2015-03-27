var sceneText = '';

$(document).ready(function() {
	// From https://gist.github.com/alanhamlett/6316427
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE' || settings.type == 'PATCH') {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		}
	});


	// Preload scene text if it's there
	sceneText = $("textarea#text").val();


	// Autosize
	$('#middle-panel textarea[name=scene-title]').autosize();
	$('#scene-panel textarea').autosize();


	// Textarea focus
	/*
	$("textarea#text").on("focus", function() {
		$("body").addClass("dimmer");
	});

	$("textarea#text").on("blur", function() {
		$("body").removeClass("dimmer");
	});
	*/


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


	// Autosave function
	function autoSave() {
		var currentText = $("textarea#text").val().trim();

		if (currentText != sceneText) {
			var storySlug = $("#main").attr("data-story-slug");
			var sceneId = $("#scene-list .scene.selected").attr("data-id");

			// The text has changed, so autosave it
			$("#middle-panel").addClass("saving");

			// Get an initial revision if it's not there
			if (!$("textarea#text").attr("data-revision-id")) {
				// New transcript for this session
				var url = "/api/story/" + storySlug + "/" + sceneId + "/add-revision/";

				var data = {
					text: currentText,
				};
			} else {
				// Update transcript for this session
				var revisionId = $("textarea#text").attr("data-revision-id");
				var url = "/api/story/" + storySlug + "/" + sceneId + "/update-revision/" + revisionId + "/";

				var data = {
					text: currentText,
				};
			}

			// Post it
			$.ajax({
				url: url,
				method: 'POST',
				contentType: 'application/json',
				data: JSON.stringify(data),
				success: function(data) {
					data = JSON.parse(data);
					$("#middle-panel").removeClass("dirty").removeClass("saving");

					$("textarea#text").attr("data-revision-id", data.id);

					// Update current cache
					sceneText = currentText;
				},
				error: function(data) {
					$("#middle-panel").addClass("error");

					console.log("error", data);
				},
			});
		} else {
			$("#middle-panel").removeClass("dirty");
		}
	}

	// Autosaving (only on writing pages)
	if ($("textarea#text").length > 0) {
		// On typing into the textarea, remove the saving notice
		$("textarea#text").on("input", function() {
			$("#middle-panel").addClass("dirty");
		});

		// Autosave every 5 seconds
		var intervalId = window.setInterval(autoSave, 5000);
	}


	// Save before closing tab
	$(window).bind('beforeunload', function() {
		// See if there's unsaved text and autosave if there is
		var currentText = $("textarea#text").val().trim();

		if (currentText != sceneText) {
			autoSave();

			confirm("Not done yet");
			// Delay a bit to let the autosave do its thing
			delay(500);
		}
	});


	// Update scene title/synopsis
	$("[name=scene-title], [name=scene-synopsis]").on("keyup", function() {
		var storySlug = $("#main").attr("data-story-slug");
		var sceneId = $("#scene-list .scene.selected").attr("data-id");

		var payload = {
			'title': $("[name=scene-title]").val().trim(),
			'synopsis': $("[name=scene-synopsis]").val().trim(),
		};

		var url = "/api/story/" + storySlug + "/" + sceneId + "/";

		$.ajax({
			url: url,
			method: 'POST',
			contentType: 'application/json',
			data: JSON.stringify(payload),
			success: function(data) {
				data = JSON.parse(data);

				// Update scene title/synopsis in scene list
				$("#scene-list .scene.selected h3").html(payload['title']);
				$("#scene-list .scene.selected .synopsis").html(payload['synopsis']);
			},
			error: function(data) {
				console.log("error", data);
			},
		});
	});


	// Add a new scene
	$("a.add-scene").on("click", function() {
		var storySlug = $("#main").attr("data-story-slug");
		var url = "/api/story/" + storySlug + "/add-scene/";

		$.ajax({
			url: url,
			method: 'POST',
			contentType: 'application/json',
			success: function(data) {
				data = JSON.parse(data);

				// Redirect to new scene
				if (data.id) {
					window.location.href = "/story/" + storySlug + "/" + data.id + "/";
				}
			},
			error: function(data) {
				console.log("error", data);
			},
		});
	});


	// Delete selected scene
	$("a.delete-scene").on("click", function() {
		var storySlug = $("#main").attr("data-story-slug");
		var sceneId = $("#scene-list .scene.selected").attr("data-id");
		var url = "/api/story/" + storySlug + "/" + sceneId + "/";

		if (confirm("Are you sure you want to delete this scene?")) {
			$.ajax({
				url: url,
				method: 'DELETE',
				contentType: 'application/json',
				success: function(data) {
					data = JSON.parse(data);

					// Redirect to story page
					window.location.href = "/story/" + storySlug + "/";
				},
				error: function(data) {
					console.log("error", data);
				},
			});
		}
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
