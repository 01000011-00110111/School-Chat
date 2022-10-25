// Dependencies
var express = require('express');
var fs = require('fs');
var http = require('http');
var path = require('path');
var socketIO = require('socket.io');

var app = express();
var server = http.Server(app);
var io = socketIO(server);

app.set('port', 5000);
app.use('/static', express.static(__dirname + '/static'));

// Routing
app.get('/', function(request, response) {
  response.sendFile(path.join(__dirname, 'static/index.html'));
});
app.get('/chat', function(request, response) {
  response.sendFile(path.join(__dirname, 'static/chat.html'));
});

// Starts the server.
server.listen(5000, function() {
  console.log('Starting server on port 5000');
});

// Add the WebSocket handlers
io.on('connection', function(socket) {
	socket.on('outgoing message', function(data) { // When a message comes in...
		console.log(data);
		io.emit('incoming message', data); // Broadcast to all clients
	});
});

/// socket.emit('server message', data);