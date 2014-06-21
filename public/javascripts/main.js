
$(document).ready(function() {

	//Connect to our server-side
	socket = io.connect('http://localhost:3000');

	$('#submit').click(function() {
		var courseList = window.atob($('#griddy_url').val().split("?link=")[1]);
		socket.emit('go', { courseList: courseList });
	});

	socket.on('adjacent classes', function(data) {
		console.log(data);
	});

	var service = new google.maps.DistanceMatrixService();

	service.getDistanceMatrix({
    origins: ["100  St. George Street, M5S 3G3"],
    destinations: ["93  Charles St. West, M5S 1K9"],
    travelMode: google.maps.TravelMode.WALKING
  }, function(response, status) {
		if (status == google.maps.DistanceMatrixStatus.OK) {
			console.log(response.rows[0].elements[0].duration);
		}
	});

});
