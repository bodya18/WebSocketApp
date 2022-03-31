var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('message_response', function( msg ) {
    console.log(msg);
})

function data_center(ev) {
    ev.preventDefault()
    msg_text = document.getElementById('send_message').value
    console.log(msg_text);
    socket.emit('message', msg_text)
}