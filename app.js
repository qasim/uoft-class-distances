
/**
 * Module dependencies.
 */

var express = require('express');
var routes = require('./routes');
var http = require('http');
var path = require('path');
var sqlite = require('sqlite3');
var tools = require('./tools');
var request = require('request');
var fs = require('fs');

var app = express();

// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.json());
app.use(express.urlencoded());
app.use(express.methodOverride());
app.use(express.cookieParser('your secret here'));
app.use(express.session());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

app.get('/', routes.index);

var server = http.createServer(app);

server.listen(app.get('port'), function() {
  console.log('Express server listening on port ' + app.get('port'));
});

//Get the database
var db = new sqlite.Database("courses.db");

//Start listening for clients
var io = require('socket.io').listen(server);

var courseList = [];
var courseInfo = {};

var fallData = [];
var springData = [];

var adjacentClasses = {};

//When a client connects
io.sockets.on('connection', function(socket) {

  socket.on('go', function(data) {

    courseList = data.courseList;
    courseList = courseList.split(",");
    courseInfo = [];
    fallData = [];
    springData = [];
    adjacentClasses = {
      fall: [],
      spring: []
    };


    modifiedCourseList = [];
    for(var i = 0; i < courseList.length; i++) {
      courseInfo[courseList[i]] = [];
      modifiedCourseList[i] = "'" + courseList[i] + "'";
    }

    var sqlList = '( ' + modifiedCourseList.join(', ') + ' )';

    console.log(sqlList);

    //Start data retrieval
    db.all("SELECT * FROM data WHERE name IN " + sqlList, function(err, rows) {
      for(var i = 0; i < rows.length; i++) {
        courseInfo[rows[i].name].push(rows[i]);
      }
      for(var i = 0; i < courseList.length; i++) {
        courseData = courseInfo[courseList[i]];
        for(var j = 0; j < courseData.length; j++) {
          if(courseData[j] != undefined) {
            var days = courseData[j].time.match(/[MTWRFS]/g);
            /*for(var x = 0; x < days.length; x++) {
              days[x] = tools.dayConversion[days[x]];
            }*/
            var times = courseData[j].time.match(/([0-9]+)[:]?[0-9]*/g);
            var startTime, endTime;
            if(times.length == 1) {
              if(times[0].match(':')) {
                timeSplit = times[0].split(':');
                startTime = timeSplit[0] * 1 + (timeSplit[1] / 60);
                endTime = startTime * 1 + 1;
              } else {
                startTime = times[0] * 1;
                endTime = times[0] * 1 + 1;
              }
            } else {
              if(times[0].match(':')) {
                timeSplit = times[0].split(':');
                startTime = timeSplit[0] * 1 + (timeSplit[1] / 60);
              } else {
                startTime = times[0] * 1;
              }
              if(times[1].match(':')) {
                timeSplit = times[1].split(':');
                endTime = timeSplit[0] * 1 + (timeSplit[1] / 60);
              } else {
                endTime = times[1] * 1;
              }
            }

            if(startTime <= 7) {
              startTime += 12;
              endTime += 12;
            }

            if(endTime <= 7) {
              endTime += 12;
            }

            var dates = [];
            for(var x = 0; x < days.length; x++) {
              var startHour = startTime;
              var startMinute = 0;
              var strStartTime = startTime + "";
              if(strStartTime.indexOf(".") > -1) {
                strStartTime = strStartTime.split(".");
                startHour = parseInt(strStartTime[0]);
                startMinute = parseInt(("0." + strStartTime[1]) * 60);
              }
              var endHour = endTime;
              var endMinute = 0;
              var strEndTime = endTime + "";
              if(strEndTime.indexOf(".") > -1) {
                strEndTime = strEndTime.split(".");
                endHour = parseInt(strEndTime[0]);
                endMinute = parseInt(("0." + strEndTime[1]) * 60);
              }
              var startDate = new Date(2014, 5, tools.dayToDate[days[x]], startHour, startMinute, 0, 0);
              var endDate = new Date(2014, 5, tools.dayToDate[days[x]], endHour, endMinute, 0, 0);
              dates.push([startDate, endDate]);
            }

            var termCode = courseData[j].course_code.substr(8, 1);

            if(termCode == "Y" || termCode == "F") {
              //Fall term
              for(var p = 0; p < dates.length; p++) {
                fallData.push({
                  info: courseData[j],
                  'date': dates[p]
                });
              }
            }

            if(termCode == "Y" || termCode == "S") {
              //Spring term
              for(var p = 0; p < dates.length; p++) {
                springData.push({
                  info: courseData[j],
                  'date': dates[p]
                });
              }
            }

          }
        }
      }

      fallData.sort(tools.dateSort);

      for(var x = 0; x < fallData.length; x++) {
        for(var y = 0; y < fallData.length; y++) {
          if(fallData[x].date[1].getTime() == fallData[y].date[0].getTime() && x != y) {
            adjacentClasses.fall.push([fallData[x], fallData[y]]);
          }
        }
      }

      springData.sort(tools.dateSort);

      console.log(JSON.stringify(springData));
      console.log(' ');

      for(var x = 0; x < springData.length; x++) {
        for(var y = 0; y < springData.length; y++) {
          if(springData[x].date[1].getTime() == springData[y].date[0].getTime() && x != y) {
            adjacentClasses.spring.push([springData[x], springData[y]]);
          }
        }
      }

      socket.emit('adjacent classes', JSON.stringify(adjacentClasses));

    });



  })

});
