//Cliente jquery: encargado de la conexion websocket con el servidor python 

// --------------------INICIALIZACION DEL CLIENTE-------------------------------

// Iniciando conexion socket
document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    // sala principal como default
    let room = ("Principal");
    joinRoom("Principal");

    // Probando los sockets
    socket.on ('connect', ()=>{
        socket.send("cliente websocket a full");
    });

// -----------------------CONTROL DE MENSAJES-------------------------------    

    // lee y envia mensajes desde el cliente al servidor
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value, 'usuario': usuario, 'room': room });

        document.querySelector('#user_message').value = '';
    };

    // Recibe y envia mensajes desde el servidor a todos los clientes
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

// ------------------CONTROL DE SALAS DE CHAT-----------------------------------

    // Seleccionar una sala
    document.querySelectorAll('.select-room').forEach(p=> {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room){
                msg = `Ya estas en la sala ${room}.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room=newRoom;
            }
        }
    });

    // Funcion para salir de un sala
    function leaveRoom(room){
        socket.emit('leave', {'usuario': usuario, 'room': room});
    }

    // Funcion para entrar a una sala
    function joinRoom(room){
        socket.emit('join', {'usuario': usuario, 'room': room});
        //borrar mensaje de pantalla
        document.querySelector('#display-message-section').innerHTML = ''
        //autocus en caja de texto del chat
        document.querySelector('#user_message').focus();
    }

    // Funcion imprimir para todos los usuarios
    function printSysMsg(msg){
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
})