$(document).ready(function() {
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


	// History panel overflow
	/*
	$("#history-panel").css("height", Math.floor($("#history-panel").height() / 2));
	*/


	// Reordering scenes in the outline
	$("#scene-list").sortable({
		placeholder: "scene placeholder",
		update: function(event, ui) {
			var order = {};
			var items = ui.item.parents("#scene-list:first").find("a.scene");

			for (var i=0; i<items.length; i++) {
				var item = $(items[i]);
				order[item.attr("data-id")] = i;
			}

			// Reorder scene numbers
			for (var i in order) {
				$("#scene-list a[data-id=" + i + "] span").html(order[i] + 1);
			}

			//var projectId = $("fieldset#name-fieldset input[type=text]").attr("data-id");
			//var url = '/transcribe/api/projects/' + projectId + '/items/update_order/';

			/*
			$.ajax({
				url: url,
				method: 'POST',
				contentType: 'application/json',
				data: JSON.stringify(order),
				success: function(data) {
				},
				error: function(data) {
					console.log("Error! :(", data);
				},
			});
			*/
		},
	});
});
