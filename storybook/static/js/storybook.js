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


	// Global hotkeys
	// --------------------------------------------------

	Mousetrap.bind('g m', _toggleMenu);


	// Tray
	// --------------------------------------------------
	
	Mousetrap.bind('a', _showTray);
	$("header[role=banner] .add").on("click", function() {
		_toggleTray();
		return false;
	});

	var field = document.querySelector('#tray textarea');
	Mousetrap(field).bind('esc', _hideTray);
	Mousetrap(field).bind(['mod+enter', 'shift+enter'], _submitTray);

	$("#tray .controls .save.button").on("click", function() {
		_submitTray();
		return false;
	});

	function _showTray() {
		// Display and focus on the tray
		$("#tray textarea").val('');

		$("#tray").slideDown(75, function() {
			$("#tray textarea").focus();
		});

		return false;
	}

	function _hideTray() {
		// Hide the tray
		$("#tray").slideUp(75, function() {
			$("#tray textarea").val('').blur();
		});

		return false;
	}

	function _toggleTray() {
		if ($("#tray:visible").length > 0) {
			_hideTray();
		} else {
			_showTray();
		}

		return false;
	}

	function _submitTray() {
		// Get value of textarea
		var text = $("#tray textarea").val().trim();

		// Make sure it's not blank
		if (text == '') return;

		// URL/key for web service
		var url = $("#tray").data("uri");

		// Payload
		var data = {
			'payload': text,
			'key': config.apiKey,
		};

		if ($("#tray").data("story-slug")) {
			data['payload'] = "::" + $("#tray").data("story-slug") + "\n\n" + data['payload'];
		}

		$.ajax({
			url: url,
			method: 'POST',
			data: data,
			success: function(data) {
				// Hide the tray
				_hideTray();

				// Reload the page
				window.location.reload();
			},
			error: function(data) {
				console.log("error :(", data);
			},
		});

		return false;
	}


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


	// Story save draft
	// --------------------------------------------------

	function _saveStoryDraft() {
		var url = $(".save-draft").attr("href");

		var data = {
			key: config.apiKey,
		};

		$.ajax({
			url: url,
			method: 'POST',
			data: data,
			success: function(data) {
                alert("New draft saved.");
			},
			error: function(data) {
				console.log("Error! :(", data);
			},
		});

		return false;
	}

	$(".save-draft.button").on("click", function() {
		_saveStoryDraft();
		return false;
	});


	// Scene save text
	// --------------------------------------------------

	// Focus on page load
	if ($(".scene-edit").length) {
		$("textarea#frame.scene-edit").focus();

		moveCaretToEnd($("textarea#frame.scene-edit")[0]);
	}

	function _cancelSceneEdit() {
		var url = $(".scene-edit").data("scene-uri");
        if (url) {
            window.location.href = url;
        }
	}

	function _saveSceneEdit() {
		var url = $(".scene-edit").data("uri");

		var text = $("textarea#frame.scene-edit").val().trim();

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

	$("html.edit .save-scene.button").on("click", function() {
		_saveSceneEdit();
		return false;
	});

	var field = document.querySelector('textarea#frame.scene-edit');
	Mousetrap(field).bind('esc', _cancelSceneEdit);
	Mousetrap(field).bind(['mod+enter', 'shift+enter'], _saveSceneEdit);


	// Story save text
	// --------------------------------------------------

	// Focus on page load
	if ($(".story-edit").length) {
		$("textarea#frame.story-edit").focus();

		moveCaretToEnd($("textarea#frame.story-edit")[0]);
	}

	function _cancelStoryEdit() {
		var url = $(".story-edit").data("story-uri");
        if (url) {
            window.location.href = url;
        }
	}

	function _saveStoryEdit() {
		var url = $(".story-edit").data("uri");

		var text = $("textarea#frame.story-edit").val().trim();

		var data = {
			text: text,
			key: config.apiKey,
		};

		$.ajax({
			url: url,
			method: 'POST',
			data: data,
			success: function(data) {
				var url = $(".story-edit").data("story-uri");
				window.location.href = url;
			},
			error: function(data) {
				console.log("Error! :(", data);
			},
		});

		return false;
	}

	$("html.edit .save-story.button").on("click", function() {
		_saveStoryEdit();
		return false;
	});

	var field = document.querySelector('textarea#frame.story-edit');
	Mousetrap(field).bind('esc', _cancelStoryEdit);
	Mousetrap(field).bind(['mod+enter', 'shift+enter'], _saveStoryEdit);


	// Story detail
	// --------------------------------------------------

	if ($(".story-detail").length) {
		Mousetrap.bind('e', function() {
			window.location.href = $(".story-detail").data("edit-uri");
		});

		Mousetrap.bind('o', function() {
			window.location.href = $(".story-detail").data("organize-uri");
		});

		Mousetrap.bind('g h', function() {
			window.location.href = $("nav[role=menu] .home").attr("href");
		});

		Mousetrap.bind('g f', function() {
			window.location.href = $("nav[role=menu] .full-story").attr("href");
		});
	}


	// Scene detail
	// --------------------------------------------------

	if ($(".scene-detail").length) {
		Mousetrap.bind('e', function() {
			window.location.href = $(".scene-detail").data("edit-uri");
		});

		Mousetrap.bind('g f', function() {
			window.location.href = $("nav[role=menu] .full-story").attr("href");
		});

		Mousetrap.bind('g h', function() {
			window.location.href = $("nav[role=menu] .story-home").attr("href");
		});

		Mousetrap.bind('g n', function() {
			var uri = $(".scene-detail").data("next-uri");
			if (uri) {
				window.location.href = uri;
			}
		});

		Mousetrap.bind('g p', function() {
			var uri = $(".scene-detail").data("prev-uri");
			if (uri) {
				window.location.href = uri;
			}
		});
	}


	// Full draft
	// --------------------------------------------------

	if ($(".full-draft").length) {
		Mousetrap.bind('g h', function() {
			window.location.href = $("nav[role=menu] .story-home").attr("href");
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
