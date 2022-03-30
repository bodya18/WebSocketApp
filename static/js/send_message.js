// const socket = new WebSocket('ws://' + location.host);

// socket.addEventListener('message', ev => {
//     ul = document.getElementById('list_msg')
//     li = document.createElement('li')
//     li.className = 'clearfix'

//     li.insertAdjacentHTML('beforeend', `
//         <div class="message-data">
//             <span class="message-data-time">NAME</span>
//         </div>
//         <div class="message my-message">${ev.data}</div>
//     `)
//     ul.appendChild(li)
//     div_chat.scrollTop = div_chat.scrollHeight
// });


// (function() {
//     div_chat = document.getElementById('div-chat-list')
//     div_chat.scrollTop = div_chat.scrollHeight
//     document.getElementById('send_message').addEventListener('keydown', function(ev) {
//         if (ev.keyCode === 13) {
//             msg_text = this.value
//             socket.send(msg_text);
//             this.value = ''
//             ul = document.getElementById('list_msg')
//             li = document.createElement('li')
//             li.className = 'clearfix'
            
//             li.insertAdjacentHTML('beforeend', `
//                 <div class="message-data text-right">
//                     <span class="message-data-time">You</span>
//                 </div>
//                 <div class="message other-message float-right">${msg_text}</div>
//             `)
//             ul.appendChild(li)
//             div_chat.scrollTop = div_chat.scrollHeight
//         }
//     });
// })();

let request = new XMLHttpRequest();

request.open("POST", "/users/add", true);   

request.setRequestHeader("Content-Type", "application/json");
let name = JSON.stringify({name:"ALEXA"})
request.addEventListener("load", function () {
    let url = JSON.parse(request.response);
    console.log(url);
});
request.send(name);
