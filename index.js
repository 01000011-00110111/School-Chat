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


// this uses socketio, a js libary (Connor add dumbed down version)
// we alrady have the majority of this done in main.py
function LoginWithReplit() {
  window.addEventListener('message', authComplete);
  var h = 500;
  var w = 350;
  var left = screen.width / 2 - w / 2;
  var top = screen.height / 2 - h / 2;

  var authWindow = window.open(
    'https://repl.it/auth_with_repl_site?domain=' + location.host,
    '_blank',
    'modal =yes, toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=' +
      w +
      ', height=' +
      h +
      ', top=' +
      top +
      ', left=' +
      left,
  );

  function authComplete(e) {
    if (e.data !== 'auth_complete') {s
      return;
    }

    window.removeEventListener('message', authComplete);

    authWindow.close();
    location.reload();
  }
}
