from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class Registro(FlaskForm):

    usuario = StringField('usuario_label',
        validators=[InputRequired(message="Escribe un nombre de usuario"),
        Length(min=4, max=25, message="El nombre de usuario debe tener entre 4 y 25 caracteres")])

    contrasena = PasswordField('contrasena_label',
        validators=[InputRequired(message="Escribe una contraseña"),
        Length(min=8, max=25, message="La contraseña debe tener entre 8 y 25 caracteres")])

    confirmar_contrasena = PasswordField('confirmar_contraseña_label',
        validators=[InputRequired(message="Escribe una contraseña"),
        EqualTo('contrasena', message="Las contraseñas deben coincidir")])

    nombre = StringField('nombre_label',
        validators=[InputRequired(message = "Escribe tu nombre"),
        Length(min=0 , max=30, message="El nombre debe contener maximo 30 caracteres")])
   
    apellido = StringField('apellido_label',
        validators=[InputRequired(message = "Escribe tu apellido"),
        Length(min=0 , max=30, message="El apellido debe contener maximo 30 caracteres")])

    edad = StringField('edad_label',
        validators=[InputRequired(message = "Escribe tu edad")])  
        
    genero = StringField('genero_label',
        validators=[InputRequired(message = "Escribe tu genero"),
        Length(min=0 , max=1, message="Escribe (F) para femenino y (M) para masculino ")])     

    boton_registro = SubmitField('Registrarse')
  
