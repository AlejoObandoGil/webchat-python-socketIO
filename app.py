# Servidor python - aplicacion principal: encargado de todo el control de usuarios y chat(registro, login, sockets, salas)

# ------------------------------LIBRERIAS---------------------------------------

# Principales: webApp, BD, cifrado hash, login de flask, websockets, hilos, fechas y hora
from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from time import strftime, localtime, gmtime
import threading
import logging
import os


# Secundarias:
from modelos import *
from formulario import *

# -----------------------CONFIGURACION DEL SERVIDOR----------------------------

app = Flask(__name__)

PUERTO = os.environ.get('PUERTO')
# PUERTO = 5000

app.secret_key = os.environ.get('SECRET')
# app.secret_key = "SECRET"

# Direccion de BD: postgres de heroku
# Usuario, contraseña, host, puerto, nombre de la BD
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# "postgres://odzwjrzlprudil:8317735ed8c2403e044449e353a227dbc9ca3a0afc17ba794f37cfc40420558d@ec2-54-161-150-170.compute-1.amazonaws.com:5432/d57q5bus76ls43"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# inicializar en BD
db = SQLAlchemy(app)
#print("\n-conexion a BD habilitada --> heroku-postgres ")

# Inicializar websockets
socketio = SocketIO(app)
#print("-websockets habilidatos \n")

# Inicializar controlador de sesion
login = LoginManager(app)
login.init_app(app)

# Lista donde almacenaremos las salas creadas, por defecto el servidor incia con 1 sola sala
LISTA_SALAS = ["Principal"]

# logging entrega informacion acerca de los hilos con mensajes en consola 
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-s) %(message)s')


# ----------------------FUNCIONES BASICAS DEL SERVIDOR-------------------------

# Ruta principal para index.html
@app.route("/", methods=['GET', 'POST'])
def index():
    logging.info("Consultando hilo de inicio de sesion")
    # Instanciamos desde formulario
    inicioForm = InicioSesion()
    # Validamos el formulario que digitamos
    if inicioForm.validate_on_submit():
        obj_usuario = User.query.filter_by(
            usuario=inicioForm.usuario.data).first()
        login_user(obj_usuario)
        # Mensaje instantaneo en pantalla
        flash("¡Bienvenido a TertuliApp. Inicia sesión o regístrate para empezar a hablar!", "success")
        # Si hay exito redirige al chat
        return redirect(url_for('chat'))

    # Si no hay exito regresa a la pagina de index
    return render_template("index.html",  form=inicioForm)


# Ruta de inicio de sesion para registro.html
@app.route("/registro", methods=['GET', 'POST'])
def registro():
    logging.info("Consultando hilo de registro")
    # Instanciamos desde formulario
    registroForm = Registro()
    # Validamos el formulario que digitamos
    if registroForm.validate_on_submit():

        usuario = registroForm.usuario.data
        contrasena = registroForm.contrasena.data
        nombre = registroForm.nombre.data
        apellido = registroForm.apellido.data
        edad = registroForm.edad.data
        genero = registroForm.genero.data

        # Cifrar la contraseña con hash
        #pbkdf2_sha256.using(round=1000, salt_size=8).hash(contrasena)
        contrasena_hash = pbkdf2_sha256.hash(contrasena)

        # En el contexto de la app agregamos lo digitado en los textFields
        # Agregamos y hacemos un commit a la BD
        with app.app_context():
            user = User(nombre=nombre, apellido=apellido, usuario=usuario,
                        contrasena=contrasena_hash, edad=edad, genero=genero)
            db.create_all()
            # db.drop_all()
            # db.session.delete(usuario)
            db.session.add(user)
            db.session.commit()
        # Si hay exito imprime en la pagina y redirige a login
        flash("¡Te has registrado en TerTuliApp, ahora puedes iniciar sesión!", "success")

        return redirect(url_for('index'))
    # Si no hay exito regresa a la pagina de registro
    return render_template("registro.html", form=registroForm)


# Ruta que recarga el cliente actual conectado
@login.user_loader
def cargar_usuario(id):
    return User.query.get(int(id))


 # Ruta para cerrar sesion
@app.route("/cerrar_sesion", methods=['GET'])
def cerrar_sesion():
    logging.info("Consultando hilo de cerrar sesion")
    logout_user()

    return redirect(url_for('index'))


# Ruta de chat para chat.html
@app.route("/chat", methods=['GET', 'POST'])
def chat():
    logging.info("Consultando hilo de chat")

    nuevaSala = ""

    # Metodo POST para validar la creacion de la nueva salida
    if request.method == 'POST':
        nuevaSala = request.form['nueva_sala']
        if nuevaSala in LISTA_SALAS:
            flash("¡La sala ya existe, elige otro nombre", "success")
        else:
            LISTA_SALAS.append(nuevaSala)

    eliminarSala = EliminarSala()
    sala = eliminarSala.input_eliminar_sala.data
    if sala in LISTA_SALAS:
        if sala != LISTA_SALAS[0]:
            LISTA_SALAS.remove(sala)

    # Instanciamos un objeto User para listar los usuarios en la BD
    user = User.query.all()
    # Numero de usuarios en la BD
    nUser = User.query.count()
    # Numero de salas creadas
    # nSala = len(LISTA_SALAS)

    # El usuario debe estar autenticado en la sesion para tener acceso al chat
    if not current_user.is_authenticated:
        flash('Por favor inicia sesion', "success")
        return redirect(url_for('index'))

    # Siempre redirige a la cuenta del mismo usuario si la sesion esta abierta
    return render_template('chat.html', usuario=current_user.usuario, rooms=LISTA_SALAS, form=eliminarSala, user=user, nUser=nUser)


# ---------------------FUNCIONES WEBSOCKETS DEL SERVIDOR------------------------

# Ruta socket que se comunica con el cliente javascript, recibe y manda el mensaje
@socketio.on('message')
def message(data):
    print(f"\n\n {data}\n\n")
    send({'msg': data['msg'], 'usuario': "[ " + data['usuario'] + " ]",
          'time_stamp': strftime("%a, %d %b %Y - %X")}, room=data['room'])


# Ruta socket que se comunica con el cliente javascript cada vez que un nuevo cliente ingresa a una sala
@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': "El usuario [ " + data['usuario'] +
          " ],  se ha unido a la sala  " + data['room'] + "."}, room=data['room'])


# Ruta socket que se comunica con el cliente javascript cada vez que un nuevo cliente sale de una sala
@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': "El usuario [ " + data['usuario'] +
          " ],  ha salido de la sala  " + data['room'] + "."}, room=data['room'])


# -------------------------------HILOS------------------------------------------

# Creando hilos
hiloInicioSesion = threading.Thread(target=index)
hiloCerrarSesion = threading.Thread(target=cerrar_sesion)
hiloRegistro = threading.Thread(target=registro)

# Ligado al hilo principal
hiloInicioSesion.daemon = True 
hiloCerrarSesion.daemon = True 
hiloRegistro.daemon = True     
                                          
# Iniciar hilo
hiloInicioSesion.start() 
hiloCerrarSesion.start() 
hiloRegistro.start() 

# Iniciar hilos antes que el hilo principal
# hiloInicioSesion.join()
# hiloCerrarSesion.join()   
# hiloRegistro.join()  
# hiloChat.join()   
    

# -----------------------------PRINCIPAL----------------------------------------

if __name__ == "__main__":
  
    # db.init_app(app)
    # app.run(debug=True)
    socketio.run(app, debug=True)



