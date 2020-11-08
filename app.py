from flask import Flask, request, render_template, session
from flask_sqlalchemy import SQLAlchemy

from wtform_registro import *
#from modelos import *

app = Flask(__name__)
app.secret_key = 'replace later'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://odzwjrzlprudil:8317735ed8c2403e044449e353a227dbc9ca3a0afc17ba794f37cfc40420558d@ec2-54-161-150-170.compute-1.amazonaws.com:5432/d57q5bus76ls43'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(25), unique=True, nullable=False)
    contrasena = db.Column(db.String(25), nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    edad = db.Column(db.String(2), nullable=False)
    genero = db.Column(db.String(1), nullable=False)

db.create_all() 

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

        user_object = User.query.filter_by(usuario=usuario).first()
        if user_object:
            return "Ya se encuentra en uso este nombre de usuario"  

        with app.app_context():     
            user = User(nombre=nombre, apellido=apellido, usuario=usuario, contrasena=contrasena, edad=edad, genero=genero)                  
            db.create_all() 
            db.session.add(user)
            db.session.commit()
            

        return "Ingresado en la base de datos"

    return render_template("index.html", form=reg_form)


if __name__ == "__main__":

    db.init_app(app)
    app.run(debug=True)