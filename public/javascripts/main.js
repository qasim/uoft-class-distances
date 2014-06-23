
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

window.day = [
	'Monday',
	'Tuesday',
	'Wednesday',
	'Thursday',
	'Friday',
	'Saturday',
	'Sunday'
]

window.formatAMPM = function(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = hours + ':' + minutes + ' ' + ampm;
  return strTime;
}

window.fillPage = function(type, courseInfo) {
	for(var i = 0; i < courseInfo.length; i++) {
		var origin = courseInfo[i][0].info.location;
		var destination = courseInfo[i][1].info.location;
		var id = 'id-' + courseInfo[i][0].info.id + '-to-' + courseInfo[i][1].info.id;

		var startDate = new Date(courseInfo[i][0].date[0]);
		var endDate = new Date(courseInfo[i][0].date[1]);
		var timeString = window.day[startDate.getDay()] + 's <em>' + formatAMPM(startDate) +
										 '</em> to <em>' + formatAMPM(endDate) + '</em>';

		var startDate2 = new Date(courseInfo[i][1].date[0]);
		var endDate2 = new Date(courseInfo[i][1].date[1]);
		var timeString2 = window.day[startDate2.getDay()] + 's <em>' + formatAMPM(startDate2) +
										 '</em> to <em>' + formatAMPM(endDate2) + '</em>';

		var mapsURL = 'http://maps.google.com/maps?dirflg=w&saddr=' +
									courseInfo[i][0].info.location + '&daddr=' +
									courseInfo[i][1].info.location;

		$('#' + type).append('\
		<table class="pair ' + id + '">\
			<tr>\
				<td>\
					<div class="class first">\
						<div class="course-code">' + courseInfo[i][0].info.name + '</div>\
						<div class="time">' + timeString + '</div>\
						<div class="location">\
							<a title="' + courseInfo[i][0].info.location + '">' + courseInfo[i][0].info.location_name + '</a>\
							</div>\
					</div>\
				</td>\
				<td rowspan="2">\
					<div class="duration-holder">\
						<a class="duration" href="' + mapsURL + '" target="_blank">...</a>\
					</div>\
				</td>\
			</tr>\
			<tr>\
				<td>\
					<div class="class first">\
						<div class="course-code">' + courseInfo[i][1].info.name + '</div>\
						<div class="time">' + timeString2 + '</div>\
						<div class="location">\
							<a title="' + courseInfo[i][1].info.location + '">' + courseInfo[i][1].info.location_name + '</a>\
							</div>\
					</div>\
				</td>\
			</tr>\
		</table>');

		if(origin != destination) {
			window.getDistanceMatrix(courseInfo[i][0], courseInfo[i][1]);
		} else {
			window.updateHtml(
				courseInfo[i][0],
				courseInfo[i][1],
				'0 mins'
			);
		}
	}
}

$(document).ready(function() {

	//Connect to our server-side
	socket = io.connect('http://localhost:3000');

	socket.on('connection', function() {
		$('.search').fadeIn('fast');
	})

	$('#griddy_url').keyup(function(event) {
		if(event.keyCode == 13) {
			$('#submit').click();
		}
	});

	$('#submit').click(function() {
		var courseList = window.atob($('#griddy_url').val().split("?link=")[1]);
		socket.emit('go', { courseList: courseList });
	});

	socket.on('adjacent classes', function(data) {
		var pairs = JSON.parse(data);
		$('#fall').html('');
		$('#spring').html('');
		$('.section-holder').stop().fadeIn('fast');

		//update
		window.fillPage('fall', pairs.fall);
		window.fillPage('spring', pairs.spring);

	});

	$('#more').click(function() {
		if($('.top-bar').height() == 48) {
			$('.top-bar').animate({
				height: 300
			}, 'fast');
			$('#more').html('(less info)');
		} else {
			$('.top-bar').animate({
				height: 48
			}, 'fast');
			$('#more').html('(more info)');
		}
	});

});
