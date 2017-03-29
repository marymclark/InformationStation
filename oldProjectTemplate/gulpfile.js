var gulp = require('gulp');

'use strict';

var process = require('child_process');

gulp.task('run', function(){
  var spawn = process.spawn;
  console.info('Starting flask server');
  var PIPE = {stdio: 'inherit'};
  spawn('python', ['server.py','runserver'], PIPE);
});