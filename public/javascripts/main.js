
$(document).ready(function() {

	//Connect to our server-side
	socket = io.connect('http://localhost:3000');

	$('#submit').click(function() {
		var courseList = window.atob($('#griddy_url').val().split("?link=")[1]);
		socket.emit('go', { courseList: courseList });
	});

});
