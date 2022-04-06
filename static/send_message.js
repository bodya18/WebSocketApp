var socket = io.connect('http://' + document.domain + ':' + location.port);
// var socket = io.connect('http://31.28.9.200:23765/');
socket.emit('connected', {
    "email": "vi@mail.ry",
    "id": 3,
    "last_message": null,
    "name": "Kew",
    "role": "User",
    "socket": null,
    "status": null
})

socket.on('admin_response', function( msg ) {
    console.log(msg);
})

function data_center(ev) {
    ev.preventDefault()
    msg_text = document.getElementById('send_message').value
    message = {
        user_id: 3,
        message: msg_text
    }
    // console.log(message);
    socket.emit('user_message', message)
}

function admin_send_message(ev) {
    ev.preventDefault()
    msg_text = document.getElementById('admin_send_message').value
    message = {
        user_id: 2,
        message: msg_text
    }
    console.log(message);
    socket.emit('admin_send_message', message)
}