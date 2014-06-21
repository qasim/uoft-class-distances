
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

//When a client connects
io.sockets.on('connection', function(socket) {

  socket.on('go', function(data) {

    courseList = data.courseList;
    courseList = courseList.split(",");
    courseInfo = [];

    modifiedCourseList = []
    for(var i = 0; i < courseList.length; i++) {
      courseInfo[courseList[i]] = undefined;
      modifiedCourseList[i] = "'" + courseList[i] + "'";
    }

    var sqlList = '( ' + modifiedCourseList.join(', ') + ' )';

    console.log(sqlList);

    //Start data retrieval
    db.all("SELECT * FROM data WHERE name IN " + sqlList, function(err, rows) {
      for(var i = 0; i < rows.length; i++) {
        courseInfo[rows[i].name] = rows[i];
      }
      for(var i = 0; i < courseList.length; i++) {
        courseData = courseInfo[courseList[i]];
        if(courseData != undefined) {
          var days = courseData.time.match(/[MTWRFS]/g);
          var times = courseData.time.match(/[0-9]+/g);
          var startTime, endTime;
          if(times.length == 1) {
            startTime = times[0] * 1;
            endTime = times[0] * 1 + 1;
          } else {
            startTime = times[0] * 1;
            endTime = times[1] * 1;
          }

          if(startTime <= 7) {
            startTime += 12;
            endTime += 12;
          }

          console.log(days, startTime, endTime);
        }
      }
    });



  })

});
