#---------------LIBRERIAS---------------
# Principales: webApp, BD, cifrado hash, login de flask, websockets
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, send

# Secundarias
from wtform_registro import *
from modelos import *

app = Flask(__name__)
app.secret_key = 'replace later'

# Direccion de BD postgres almacenado en heroku
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://odzwjrzlprudil:8317735ed8c2403e044449e353a227dbc9ca3a0afc17ba794f37cfc40420558d@ec2-54-161-150-170.compute-1.amazonaws.com:5432/d57q5bus76ls43'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

socketio = SocketIO(app)


login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):

    # User.query.filter_by(id=id).first()
    return User.query.get(int(id))


@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = Registro()
    if reg_form.validate_on_submit():

        usuario = reg_form.usuario.data
        contrasena = reg_form.contrasena.data
        nombre = reg_form.nombre.data
        apellido = reg_form.apellido.data
        edad = reg_form.edad.data
        genero = reg_form.genero.data

        #pbkdf2_sha256.using(round=1000, salt_size=8).hash(contrasena)
        contrasena_hash = pbkdf2_sha256.hash(contrasena)

        with app.app_context():
            user = User(nombre=nombre, apellido=apellido, usuario=usuario,
                        contrasena=contrasena_hash, edad=edad, genero=genero)
            db.create_all()
            db.session.add(user)
            db.session.commit()

        flash("¡Te has registrado en TerTuliApp, ahora puedes iniciar sesion!", "success")

        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = InicioSesion()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(
            usuario=login_form.usuario.data).first()
        login_user(user_object)

        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)


@app.route("/chat", methods=['GET', 'POST'])
def chat():

    #if not current_user.is_authenticated:
        #flash("Por favor inicia sesion para acceder a TerTuliApp", )
        #return redirect(url_for('login'))

    return render_template('chat.html') 
    #"Escribe en el chat o crea una nueva sala"


@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash("¡Has cerrado la sesion!")
    return redirect(url_for('login'))


@socketio.on('message')
def message(data):

    print(f"\n\n{data}\n\n")

    send(data)


if __name__ == "__main__":

    db.init_app(app)
    socketio.run(app, debug=True)
    #app.run(debug=True)
