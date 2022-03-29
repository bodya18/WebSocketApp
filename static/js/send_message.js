var socket = io.connect('http://' + document.domain + ':' + location.port);

(function() {
    div_chat = document.getElementById('div-chat-list')
    div_chat.scrollTop = div_chat.scrollHeight
    document.getElementById('send_message').addEventListener('keydown', function(ev) {
        if (ev.keyCode === 13) {
            msg_text = this.value

            socket.emit('message', msg_text)

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
            div_chat.scrollTop = div_chat.scrollHeight
        }
    });
})();


socket.on('message_response', function( msg ) {
    ul = document.getElementById('list_msg')
    li = document.createElement('li')
    li.className = 'clearfix'
    
    li.insertAdjacentHTML('beforeend', `
        <div class="message-data">
            <span class="message-data-time">NAME</span>
        </div>
        <div class="message my-message">${msg}</div>
    `)
    ul.appendChild(li)
    div_chat.scrollTop = div_chat.scrollHeight
})