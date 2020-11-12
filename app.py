# Aplicacion principal que hace el trabajo del servidor 

# ------------------------------LIBRERIAS---------------------------------------

# Principales: webApp, BD, cifrado hash, login de flask, websockets
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, send, emit
from time import strftime, localtime, gmtime

# Secundarias: 
from wtform_registro import *
from modelos import *


# -------------------------Inicializacion del servidor--------------------------

app = Flask(__name__)
app.secret_key = 'replace later'

# Direccion de BD: postgres de heroku
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://odzwjrzlprudil:8317735ed8c2403e044449e353a227dbc9ca3a0afc17ba794f37cfc40420558d@ec2-54-161-150-170.compute-1.amazonaws.com:5432/d57q5bus76ls43'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# inicializar BD 
db = SQLAlchemy(app)
print("\n-Conexion a BD habilitada -> heroku-postgres ")

# inicializar websockets
socketio = SocketIO(app)
print("-websockets habilitados \n")

# inicializar controlador de sesion 
login = LoginManager(app)
login.init_app(app)


# ---------------------------Rutas y controladores------------------------------

@login.user_loader
def load_user(id):

    # User.query.filter_by(id=id).first()
    return User.query.get(int(id))


# Ruta principal para index.html 
@app.route("/", methods=['GET', 'POST'])
def index():

    # Objeto de la clase registro
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
        contrasena_hash = pbkdf2_sha256.hash(contrasena)

        # En el contexto de la app agregamos lo digitado en los textFields
        # Agregamos y hacemos un commit a la BD
        with app.app_context():
            user = User(nombre=nombre, apellido=apellido, usuario=usuario,
                        contrasena=contrasena_hash, edad=edad, genero=genero)
            db.create_all()
            db.session.add(user)
            db.session.commit()
        # Si hay exito imprime en la pagina y redirige a login
        flash("¡Te has registrado en TerTuliApp, ahora puedes iniciar sesion!", "success")
        print("-Usuario registrado en la BD \n")

        return redirect(url_for('login'))
    
    # Si no hay exito regresa a la pagina de registro
    return render_template("index.html", form=reg_form)


# Ruta de inicio de sesion para login.html
@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = InicioSesion()
    # Validamos el formulario que digitamos 
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(
            usuario=login_form.usuario.data).first()
        login_user(user_object)

        # Si hay exito imprime en la pagina y redirige al chat
        flash("¡Bienvenido a TertuliApp. Escribe en el chat o crea una nueva sala!", "success")
        print("-Nuevo inicio de sesion de usuario \n")
        
        return redirect(url_for('chat'))

    # Si no hay exito regresa a la pagina de login
    return render_template("login.html", form=login_form)


# Ruta de chat para chat.html
@app.route("/chat", methods=['GET', 'POST'])
def chat():

    # El usuario debe estar autenticado en la sesion para tener acceso al chat
    #if not current_user.is_authenticated:
        #flash("Por favor inicia sesion para acceder a TerTuliApp", )
        #return redirect(url_for('login'))

    return render_template('chat.html', usuario=current_user.usuario) 
    

# Ruta para cerrar sesion redirige al incio
@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash("¡Has cerrado la sesion!")
    return redirect(url_for('login'))


# Ruta para enviar los mensajes con Socketio
@socketio.on('message')
def message(data):

    print(f"\n\n{data}\n\n")

    send({'msg': data['msg'], 'usuario': data['usuario'], 'time_stamp': strftime('%b-%d %I:%M%p', localtime())})



# ---------------PRINCIPAL-------------------

if __name__ == "__main__":

    db.init_app(app)
    print("----El servidor esta conectado...\n")
    socketio.run(app, debug=True)
    #app.run(debug=True)
