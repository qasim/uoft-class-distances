
window.getDistanceMatrix = function (firstClass, secondClass) {
	var origin = firstClass.info.location;
	var destination = secondClass.info.location;
	window.service.getDistanceMatrix({
    origins: [origin],
    destinations: [destination],
    travelMode: google.maps.TravelMode.WALKING
  }, function (response, status) {

		if (status == google.maps.DistanceMatrixStatus.OK) {
			window.updateHtml(
				firstClass,
				secondClass,
				response.rows[0].elements[0].duration.text
			);
		}

	});
}

window.updateHtml = function(firstClass, secondClass, duration) {
	var id = 'id-' + firstClass.info.id + '-to-' + secondClass.info.id;
	$('table.' + id + ' .duration').html(duration);
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

		for(var i = 0; i < pairs.fall.length; i++) {
			var origin = pairs.fall[i][0].info.location;
			var destination = pairs.fall[i][1].info.location;
			var id = 'id-' + pairs.fall[i][0].info.id + '-to-' + pairs.fall[i][1].info.id;
			$('#fall').append('\
			<table border="1" cellpadding="8" class="' + id + '">\
				<tr>\
					<td>' + pairs.fall[i][0].info.name + '</td>\
					<td rowspan="2" class="duration">...</td>\
				</tr>\
				<tr>\
					<td>' + pairs.fall[i][1].info.name + '</td>\
				</tr>\
			</table><br />');

			if(origin != destination) {
				window.getDistanceMatrix(pairs.fall[i][0], pairs.fall[i][1]);
			} else {
				window.updateHtml(
					pairs.fall[i][0],
					pairs.fall[i][1],
					'0 mins'
				);
			}

		}

	});

});
