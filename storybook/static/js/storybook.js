// CSRF stuff

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
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

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }

		xhr.setRequestHeader('X-API-KEY', config.api_key);
    }
});


$(document).ready(function() {
	// Menu code
	// --------------------------------------------------

	function _toggleMenu() {
		$("body").toggleClass("active-nav");
	}

	function _showMenu() {
		$("body").addClass("active-nav");
	}

	function _hideMenu() {
		$("body").removeClass("active-nav");
	}

	$("a.menu").on("click touchstart", function() {
		_toggleMenu();
		return false;
	});

	$(".mask").on("click touchstart", function(e) {
		_hideMenu();
		return false;
	});


	// Hotkeys
	// --------------------------------------------------

	Mousetrap.bind('g m', _toggleMenu);


	// Sorting scenes (organize page)
	// --------------------------------------------------

	if ($(".scenes.sortable").length) {
		var sceneList = $(".scenes.sortable")[0];
		var sortable = new Sortable(sceneList, {
			draggable: ".scene",
			handle: ".handle",
			onUpdate: function(e) {
				var scene = $(e.scene);
				var sceneParent = $(".scenes");
				var scenes = sceneParent.find(".scene");
				var order = [];

				for (var i=0; i<scenes.length; i++) {
					var s = $(scenes[i]);
					order.push(parseInt(s.attr("data-id")));
				}

				var url = sceneParent.data("sort-uri");

				var data = {
					ids: order.join(','),
					key: config.apiKey,
				};

				$.ajax({
					url: url,
					method: 'POST',
					data: data,
					success: function(data) {
						// Renumber the scenes

						for (var i=0; i<scenes.length; i++) {
							$(scenes[i]).find(".num").html(i + 1);
						}
					},
					error: function(data) {
						console.log("Error! :(", data);
					},
				});
			},
		});
	}


	// Scene save text
	// --------------------------------------------------

	// Focus on page load
	if ($(".scene-edit").length) {
		$(".scene-edit .text textarea").focus();

		moveCaretToEnd($(".scene-edit .text textarea")[0]);
	}

	function _cancelSceneEdit() {
		var url = $(".scene-edit").data("scene-uri");
		window.location.href = url;
	}

	function _saveSceneEdit() {
		var url = $(".scene-edit").data("uri");

		var text = $(".scene-edit .text textarea").val().trim();

		var data = {
			text: text,
			key: config.apiKey,
		};

		$.ajax({
			url: url,
			method: 'POST',
			data: data,
			success: function(data) {
				var url = $(".scene-edit").data("scene-uri");
				window.location.href = url;
			},
			error: function(data) {
				console.log("Error! :(", data);
			},
		});

		return false;
	}

	$(".scene-edit .save.button").on("click", function() {
		_saveSceneEdit();
		return false;
	});

	var field = document.querySelector('.scene-edit .text textarea');
	Mousetrap(field).bind('esc', _cancelSceneEdit);
	Mousetrap(field).bind(['mod+enter', 'shift+enter'], _saveSceneEdit);


	// Scene detail
	// --------------------------------------------------

	if ($(".story-detail").length) {
		Mousetrap.bind('e', function() {
			window.location.href = $(".story-detail").data("edit-uri");
		});

		Mousetrap.bind('g h', function() {
			window.location.href = $(".story-detail").data("parent-uri");
		});
	}


	// Scene detail
	// --------------------------------------------------

	if ($(".scene-detail").length) {
		Mousetrap.bind('e', function() {
			window.location.href = $(".scene-detail").data("edit-uri");
		});

		Mousetrap.bind('g h', function() {
			window.location.href = $(".scene-detail").data("parent-uri");
		});
	}
});

function moveCaretToEnd(el) {
	if (typeof el.selectionStart == "number") {
		el.selectionStart = el.selectionEnd = el.value.length;
	} else if (typeof el.createTextRange != "undefined") {
		el.focus();
		var range = el.createTextRange();
		range.collapse(false);
		range.select();
	}
}
