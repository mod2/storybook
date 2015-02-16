$(document).ready(function() {
	$("a.toggle-synopses").on("click", function() {
		$("#outline-panel").toggleClass("show-synopses");
		return false;
	});

	// Autosize
	$('#scene-panel textarea').autosize();
});
