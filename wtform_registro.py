from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class Registro(FlaskForm):

    usuario = StringField('usuario_label',
        validators=[InputRequired(message="Requiere un nombre de usuario"),
        Length(min=4, max=25, message="El nombre de usuario debe tener entre 4 y 25 caracteres")])
    contraseña = PasswordField('contraseña_label',
        validators=[InputRequired(message="Requiere una contraseña"),
        Length(min=4, max=25, message="La contraseña debe tener entre 4 y 25 caracteres")])
    confirmar_contraseña = PasswordField('confirmar_contraseña_label',
        validators=[InputRequired(message="Requiere una contraseña"),
        EqualTo('contraseña', message="La contraseña debe coincidir")])

    boton_registro = SubmitField('Registrarse')
  
