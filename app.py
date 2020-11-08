from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from wtform_registro import *
from modelos import *

app = Flask(__name__)
app.secret_key = 'replace later'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://odzwjrzlprudil:8317735ed8c2403e044449e353a227dbc9ca3a0afc17ba794f37cfc40420558d@ec2-54-161-150-170.compute-1.amazonaws.com:5432/d57q5bus76ls43'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  

db = SQLAlchemy(app)

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

        with app.app_context():     
            user = User(nombre=nombre, apellido=apellido, usuario=usuario, contrasena=contrasena, edad=edad, genero=genero)                  
            db.create_all() 
            db.session.add(user)
            db.session.commit()
            
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = InicioSesion()
    if login_form.validate_on_submit():
        return "¡Nuevo inicio de sesion. Ahora estas conectado!"

    return render_template("login.html", form=login_form)


if __name__ == "__main__":

    db.init_app(app)
    app.run(debug=True)