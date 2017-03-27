var main = angular.module('main',['angularMoment']);

main.controller('ChatController', ['$scope', 'moment', function($scope) {
    /* initialize at root */
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    /* initiate vars */
    $scope.messages = [];
    $scope.name = '';
    $scope.filter = false;

    socket.on('connect', function() {
        /* for debugging purposes */
        console.log('app.js: Socket.io connected.');
    });

    socket.on('message', function(msg,src) {
        /* implement moment.js */
        msg.time = moment(msg.time)
        /* add messages to scope */
        $scope.messages.push(msg);
        console.log(msg.author + ': ' + msg.txt + ' (' + msg.time + ')');
        $scope.$apply();
        /* change scroll location after sending message */
        var elem = document.getElementById('message-pane');
        elem.scrollTop = elem.scrollHeight;
    });

    $scope.find = function find() {
        console.log('Toggling chat filter...');
        $scope.filter = !$scope.filter;
        $scope.$apply;
    }

    $scope.chatfilter = function (m) {
        if ($scope.filter) {
            return m.txt.toLowerCase().includes($scope.text.toLowerCase());
        }
        return true;
    }

    $scope.send = function send() {
        console.log ('Sending message:', $scope.text);
        /* send to server.py @socket.on('message') */
        if($scope.text.length > 0) {
            socket.emit('message', $scope.text);
        }
        /* reset text in field */
        $scope.text = '';
    };
}]);

