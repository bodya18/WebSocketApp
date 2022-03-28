const socket = new WebSocket('ws://' + location.host + '/test');

socket.addEventListener('message', ev => {
    console.log(ev.data);
    ul = document.getElementById('list_msg')
    li = document.createElement('li')
    li.className = 'clearfix'
    
    li.insertAdjacentHTML('beforeend', `
        <div class="message-data">
            <span class="message-data-time">NAME</span>
        </div>
        <div class="message my-message">${msg_text}</div>
    `)
    ul.appendChild(li)
    console.log(ul);
});


(function() {
    document.getElementById('send_message').addEventListener('keydown', function(ev) {
        if (ev.keyCode === 13) {
            msg_text = this.value
            console.log(msg_text);
            socket.send(msg_text);
            this.value = ''
            ul = document.getElementById('list_msg')
            li = document.createElement('li')
            li.className = 'clearfix'
            
            li.insertAdjacentHTML('beforeend', `
                <div class="message-data text-right">
                    <span class="message-data-time">You</span>
                </div>
                <div class="message other-message float-right">${msg_text}</div>
            `)
            ul.appendChild(li)
            console.log(ul);
        }
    });
})();