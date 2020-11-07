from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from wtform_registro import *
from modelos import *

app = Flask(__name__)
app.secret_key = 'replace later'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mciebhbvvwkyje:8c7c356e012a9348f9e5257b90e5bad7b0f60085da2f292420464b2edf0abace@ec2-52-5-176-53.compute-1.amazonaws.com:5432/dbor0jn7c62572'
db = SQLAlchemy(app)


@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = Registro()
    if reg_form.validate_on_submit():

        nombre = reg_form.nombre.data
        apellido = reg_form.apellido.data
        usuario = reg_form.usuario.data
        contraseña = reg_form.contraseña.data
        edad = reg_form.edad.data
        genero = reg_form.genero.data

        user_object = Usuario.query.filter_by(usuario=usuario).first()
        if user_object:
            return "Ya se encuentra en uso este nombre de usuario"

        user = Usuario(nombre=nombre, apellido = apellido, usuario=usuario, contraseña=contraseña, edad = edad, genero = genero)
        db.session.add(user)
        db.session.commit()
        return "Ingresado a la base de datos"

    return render_template("index.html", form=reg_form)


if __name__ == "__main__":

    app.run(debug=True)