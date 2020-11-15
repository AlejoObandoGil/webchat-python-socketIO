document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    let room = ("Principal");
    joinRoom("Principal");

    socket.on ('connect', ()=>{
        socket.send("Todo bien en casa");
    });

    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value, 'usuario': usuario, 'room': room });

        document.querySelector('#user_message').value = '';
    }

    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        if (data.usuario){
            span_username.innerHTML = data.usuario;
            span_timestamp.innerHTML=data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p); 
        } else {
            printSysMsg(data.msg);
        }
         
    });


    document.querySelectorAll('.select-room').forEach(p=> {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room){
                msg = `You are already in ${room} room.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room=newRoom;
            }
        }
    });

    function leaveRoom(room){
        socket.emit('leave', {'usuario': usuario, 'room': room});
    }

    function joinRoom(room){
        socket.emit('join', {'usuario': usuario, 'room': room});
        //borrar mensaje de pantalla
        document.querySelector('#display-message-section').innerHTML = ''
        //autofocus en caja de texto del chat
        document.querySelector('#user_message').focus();
    }

    function printSysMsg(msg){
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
})





