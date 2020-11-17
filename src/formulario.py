#Codigo que controla la logica de validacion de formularios de registros y de inicio de sesion

#--------LIBRERIAS-------

#PRINCIPALES: formularios flask, validaciones y logica de formulario wrform, cifrado de contraseñas hash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

#Secundarias: 
from modelos import User

#Funcion que se encarga de validar el inicio de sesion 
def invalid_credentials(form, field):
    
    usuario_entered = form.usuario.data
    contrasena_entered = field.data

    #Validamos si existe un usuario en la BD
    user_object = User.query.filter_by(usuario=usuario_entered).first()
    if user_object is None:
        raise ValidationError("Usuario o contraseña incorrecto")

    #si existe pasa al elif y valida si la contraseña no es correcta
    elif not pbkdf2_sha256.verify(contrasena_entered, user_object.contrasena):
        raise ValidationError("Usuario o Contraseña incorrecto")

#clase que recibe y controla la validacion del formulario de registro index.html: si el usuario ya existe, si las contraseñas son iguales y que no exceda los parametros establecidos 
class Registro(FlaskForm):
    '''Registratio form'''

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
        validators=[InputRequired(message = "Escribe tu edad"),
        Length(min=0 , max=2, message="La edad debe contener maximo 2 numeros")])
        
    genero = StringField('genero_label',
        validators=[InputRequired(message = "Escribe tu genero"),
        Length(min=0 , max=1, message="Escribe (F) para femenino y (M) para masculino ")])     

    boton_registro = SubmitField('Registrarse')

#metodo que valida si el usuario ya existe en la BD antes de registrarlo
    def validate_usuario(self, usuario):
        user_object = User.query.filter_by(usuario=usuario.data).first()
        if user_object:
            raise ValidationError("El usuario ya existe. Elige otro nombre de usuario")

# Clase que recibe lo digitado en el login.html y llama la funcion invalid_credentials para validar lo recibido
class InicioSesion(FlaskForm):

    usuario = StringField ('usuario_label',
         validators=[InputRequired(message="Usuario requerido")])   

    contrasena = PasswordField('contrasena_label',
         validators= [InputRequired(message="Contraseña requerida"),
         invalid_credentials])

    boton_inicio = SubmitField('Iniciar Sesión')         