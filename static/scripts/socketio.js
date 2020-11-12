document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    socket.on ('connect', ()=>{
        socket.send("vive en una piña debajo del mar, eto eun pari por debajo el agua");
    });

    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');
        span_username.innerHTML = data.usuario;
        span_timestamp.innerHTML=data.time_stamp;
        p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
        document.querySelector('#display-message-section').append(p);

        console.log(`Message received: ${data}`)   
    })

    socket.on('some-event', data => {
        console.log(data);
    });

    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value, 'usuario': usuario});
    }
})