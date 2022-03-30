const socket = new WebSocket('ws://' + location.host);

socket.addEventListener('message', ev => {
    console.log(ev.data);
});

function data_center(ev) {
    ev.preventDefault()
    msg = document.getElementById('send_message').value
    console.log(msg);
    socket.send(msg);
}