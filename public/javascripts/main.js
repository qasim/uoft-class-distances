
window.getDistanceMatrix = function (firstClass, secondClass) {
	var origin = firstClass.info.location;
	var destination = secondClass.info.location;
	window.service.getDistanceMatrix({
    origins: [origin],
    destinations: [destination],
    travelMode: google.maps.TravelMode.WALKING
  }, function (response, status) {

		if (status == google.maps.DistanceMatrixStatus.OK) {
			console.log([
				firstClass.info.name,
				secondClass.info.name,
				response.rows[0].elements[0].duration
			]);
		}

	});
}

window.service = new google.maps.DistanceMatrixService();

$(document).ready(function() {

	//Connect to our server-side
	socket = io.connect('http://localhost:3000');

	$('#submit').click(function() {
		var courseList = window.atob($('#griddy_url').val().split("?link=")[1]);
		socket.emit('go', { courseList: courseList });
	});

	socket.on('adjacent classes', function(data) {
		var pairs = JSON.parse(data);
		console.log(pairs);
		for(var i = 0; i < pairs.spring.length; i++) {
			var origin = pairs.spring[i][0].info.location;
			var destination = pairs.spring[i][1].info.location;
			console.log(origin, destination);
			if(origin != destination) {
				window.getDistanceMatrix(pairs.spring[i][0], pairs.spring[i][1]);
			}

		}
	});

});
