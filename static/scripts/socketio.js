document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    socket.on ('connect', ()=>{
        socket.send("Estoy conectado");
    });

    socket.on('message', data => {
        console.log(`Messaage received: ${data}`)
    
    })
})