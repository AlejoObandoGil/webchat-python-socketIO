# Codigo que controla la logica de validacion de formularios de registros y de incio de sesion

# ---------------LIBRERIAS---------------

# principales: formularios de flask, validaciones y logica del formulario con wtform, cifrado hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, ValidationError
from passlib.hash import pbkdf2_sha256

# secundarias:
from modelos import User

# Funcion que se encarga de validar el inicio de sesion de usuario
def invalid_credentials(formulario, archivo):

    validar_usuario = formulario.usuario.data
    validar_contrasena = archivo.data

    # Validamos si el usuario existe en la BD
    user_object = User.query.filter_by(usuario=validar_usuario).first()
    if user_object is None:
        raise ValidationError("¡El usuario que has ingresado no existe!")

    # Si existe pasa al elif y valida si la contraseña no es correcta
    elif not pbkdf2_sha256.verify(validar_contrasena, user_object.contrasena):
        raise ValidationError(
            "¡La contraseña que has ingresado es incorrecta!")


# Clase que recibe y controla la validacion del formulario de registro index.html: si el usuario ya existe, si las contraseñas son iguales y que no exceda los parametros establecidos 
class Registro(FlaskForm):

    usuario = StringField('usuario_label',
                          validators=[InputRequired(message="Escribe un nombre de usuario"),
                                      Length(min=4, max=25, message="El nombre de usuario debe tener entre 4 y 25 caracteres")])

    contrasena = PasswordField('contrasena_label',
                               validators=[InputRequired(message="Escribe una contraseña"),
                                           Length(min=8, max=25, message="La contraseña debe tener entre 8 y 25 caracteres")])

    confirmar_contrasena = PasswordField('confirmar_contrasena_label',
                                         validators=[InputRequired(message="Escribe una contraseña"),
                                                     EqualTo('contrasena', message="Las contraseñas deben coincidir")])

    nombre = StringField('nombre_label',
                         validators=[InputRequired(message="Escribe tu nombre"),
                                     Length(min=0, max=30, message="El nombre debe contener maximo 30 caracteres")])

    apellido = StringField('apellido_label',
                           validators=[InputRequired(message="Escribe tu apellido"),
                                       Length(min=0, max=30, message="El apellido debe contener maximo 30 caracteres")])

    edad = StringField('edad_label',
                       validators=[InputRequired(message="Escribe tu edad")])

    genero = StringField('genero_label',
                         validators=[InputRequired(message="Escribe tu genero"),
                                     Length(min=0, max=1, message="Escribe (F) para femenino y (M) para masculino ")])

    boton_registro = SubmitField('Registrarse')
    
    # Metodo que valida si el usuario ya existe enla BD antes de registrarlo
    def validate_usuario(self, usuario):

        user_object = User.query.filter_by(usuario=usuario.data).first()
        if user_object:
            raise ValidationError(
                "El nombre de usuario ya existe. Elige otro")


# Clase que recibe lo digitado en el login.html y llama la funcion invalid_credentials para validar lo recibido
class InicioSesion(FlaskForm):

    usuario = StringField('usuario_label',
                          validators=[InputRequired(message='Escribe un usuario')])

    contrasena = PasswordField('contrasena_label',
                               validators=[InputRequired(message='Escribe una contraseña'),
                                           invalid_credentials])

    boton_inicio_sesion = SubmitField('Iniciar sesion')
