# Servidor python - aplicacion principal: encargado de todo el control de usuarios y chat  

# ------------------------------LIBRERIAS---------------------------------------

# Principales: webApp, BD, cifrado hash, login de flask, websockets
from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from time import strftime, gmtime

# secundarias:
from modelos import *
from formulario import *

# -----------------------INICIALIZACION DEL SERVIDOR----------------------------

app = Flask(__name__)
app.secret_key = 'replace later'

# Direccion de BD: postgres de heroku
#usuario, contraseña, host, puerto, nombre de la BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mciebhbvvwkyje:8c7c356e012a9348f9e5257b90e5bad7b0f60085da2f292420464b2edf0abace@ec2-52-5-176-53.compute-1.amazonaws.com:5432/dbor0jn7c62572'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# inicializar en BD
db = SQLAlchemy(app)
#print("\n-conexion a BD habilitada --> heroku-postgres ")

# Inicializar websockets
socketio = SocketIO(app)
ROOMS =["Principal", "Nueva sala"]
#print("-websockets habilidatos \n")

# inicializar controlador de sesion 
login = LoginManager(app)
login.init_app(app)

# ----------------------RUTAS DE LOGIN DEL SERVIDOR--------------------------

#ruta que recarga el cliente actual conectado
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# ruta principal para index.html
@app.route("/", methods=['GET', 'POST'])
def index():
    #instanciamos desde formulario
    inicio_form = InicioSesion()
    # Validamos el formulario que digitamos
    if inicio_form.validate_on_submit():
        user_object = User.query.filter_by(
            usuario=inicio_form.usuario.data).first()
        login_user(user_object)
        #mensaje instantaneo en pantalla
        flash("¡Bienvenido a TertuliApp. Inicia sesion o registrate para empezar a hablar!", "success")
        # Si hay exito redirige al chat
        return redirect(url_for('chat'))
        
    # Si no hay exito regresa a la pagina de index
    return render_template("index.html",  form=inicio_form)


# Ruta de inicio de sesion para registro.html
@app.route("/registro", methods=['GET', 'POST'])
def registro():
    #instanciamos desde formulario
    reg_form = Registro()
    # Validamos el formulario que digitamos
    if reg_form.validate_on_submit():

        usuario = reg_form.usuario.data
        contrasena = reg_form.contrasena.data
        nombre = reg_form.nombre.data
        apellido = reg_form.apellido.data
        edad = reg_form.edad.data
        genero = reg_form.genero.data

        # Cifrar la contraseña con hash
        #pbkdf2_sha256.using(round=1000, salt_size=8).hash(contrasena)
        hashed_pswd = pbkdf2_sha256.hash(contrasena)

        # En el contexto de la app agregamos lo digitado en los textFields
        # Agregamos y hacemos un commit a la BD
        with app.app_context():
            user = User(nombre=nombre, apellido=apellido, usuario=usuario,
                        contrasena=hashed_pswd, edad=edad, genero=genero)
            db.create_all()
            db.session.add(user)
            db.session.commit()
        # Si hay exito imprime en la pagina y redirige a login
        flash("¡Te has registrado en TerTuliApp, ahora puedes iniciar sesion!", "success")
       
        return redirect(url_for('index'))
    # Si no hay exito regresa a la pagina de registro
    return render_template("registro.html", form=reg_form)


# Ruta de chat para chat.html
@app.route("/chat", methods=['GET', 'POST'])
def chat(): 
    # El usuario debe estar autenticado en la sesion para tener acceso al chat
    if not current_user.is_authenticated:
        flash('Por favor inicia sesion', "success")
        return redirect(url_for('index'))
    # Siempre redirige a la cuenta del mismo usuario si la sesion esta abierta
    return render_template('chat.html', usuario = current_user.usuario, rooms=ROOMS)


 # Ruta para cerrar sesion 
@app.route("/logout", methods=['GET'])
def logout():
    logout_user()

    return redirect(url_for('index'))


# ---------------------RUTAS DE WEBSOCKETS DEL SERVIDOR-------------------------

# Ruta socket que se comunica con el cliente y recibe y manda el mensaje
@socketio.on('message')
def message(data):
    print(f"\n\n {data}\n\n")
    send({'msg': data['msg'], 'usuario': data ['usuario'], 'time_stamp': strftime("%a, %d %b %Y - %H:%M:%S", gmtime())}, room=data['room'])


# Ruta socket que se comunica con el cliente cada vez que un nuevo cliente ingresa a una sala 
@socketio.on('join')
def join(data):
    join_room(data['room']) 
    send({'msg': data['usuario'] + "  Se ha unido a la sala  " + data['room'] + "."}, room=data['room'])   


# Ruta socket que se comunica con el cliente cada vez que un nuevo cliente sale de una sala 
@socketio.on('leave')
def leave(data):    
    leave_room(data['room'])
    send({'msg': data['usuario'] + "  Ha salido de la sala  " + data['room'] + "."}, room=data['room'])

# -----------------------------PRINCIPAL----------------------------------------

if __name__ == "__main__":

    db.init_app(app)
    socketio.run(app, debug=True)
    #app.run(debug=True)
