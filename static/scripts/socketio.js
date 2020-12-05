//Cliente javascript: encargado de la conexion websocket con el servidor python

// ------------------------CONFIGURACION DEL CLIENTE----------------------------

// Iniciando conexion 
document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // sala principal como default
    let sala = ("Principal");
    joinRoom("Principal");

    // Probando los sockets
    socket.on('connect', () => {
        socket.send("cliente websocket conectado y melo mi so...");
    });

    // ----------------------CONTROL DE MENSAJES--------------------------------

    // lee y envia mensajes desde el cliente al servidor
    document.querySelector('#enviar-mensaje').onclick = () => {
        socket.send({ 'msg': document.querySelector('#nuevo-mensaje').value, 'usuario': usuario, 'room': sala });

        document.querySelector('#nuevo-mensaje').value = '';
    };

    // Recibe y envia mensajes desde el servidor a todos los clientes
    socket.on('message', data => {
        // Definimos variables tipo html(p, span, br)
        const p = document.createElement('p');
        const span_usuario = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        if (data.usuario) {
            // Creamos una cadena donde mostraremos todo el mensaje a los clientes
            span_usuario.innerHTML = data.usuario;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_usuario.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#mostrar-mensajes').append(p);
        } else {
            printMsg(data.msg);
        }

    });

    // ------------------CONTROL DE SALAS DE CHAT-------------------------------

    // Seleccionar una sala
    document.querySelectorAll('.seleccionar-sala').forEach(p => {
        p.onclick = () => {
            // Si hae click sobre una de las salas
            let nuevaSala = p.innerHTML;
            // SI es la misma salsa imprime mensaje
            if (nuevaSala == sala) {
                msg = `Ya estas en la sala ${sala}.`;
                printSysMsg(msg);
                //si no ingresa  ala nueva sala y sale de la anterior, luego actualizamos sala
            } else {
                leaveRoom(sala);
                joinRoom(nuevaSala);
                sala = nuevaSala;
            }
        }
    });

    // Funcion para salir de una sala
    function leaveRoom(sala) {
        socket.emit('leave', { 'usuario': usuario, 'room': sala });
    }

    // Funcion para entrar a una sala
    function joinRoom(sala) {
        socket.emit('join', { 'usuario': usuario, 'room': sala });
        //borrar mensaje de pantalla
        document.querySelector('#mostrar-mensajes').innerHTML = ''
        //autofocus en caja de texto del chat
        document.querySelector('#nuevo-mensaje').focus();
    }

    // Funcion imprimir para todos los usuarios
    function printMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#mostrar-mensajes').append(p);
    }
})