# Codigo por parte del cliente que controla la logica de validacion de formularios de registros y de inicio de sesion de usuario

# ------------------------------LIBRERIAS---------------------------------------

# PRINCIPALES: formularios flask, validaciones y logica de formulario wrform, cifrado de contraseñas hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

# Secundarias:
from modelos import User


# -----------------FUNCIONES Y CLASES TIPO FLASKFORM----------------------------

# Funcion que se encarga de validar el inicio de sesion
def validarUsuario(u, c):

    usuario_input = u.usuario.data
    contrasena_input = c.data

    # Validamos si existe un usuario en la BD
    user_object = User.query.filter_by(usuario=usuario_input).first()
    if user_object is None:
        raise ValidationError(
            "El nombre de usuario es incorrecto. Intenta de nuevo")

    # si existe pasa al elif y valida si la contraseña no es correcta
    elif not pbkdf2_sha256.verify(contrasena_input, user_object.contrasena):
        raise ValidationError("La contraseña es incorrecta. Intenta de nuevo")


# clase que recibe y controla la validacion del formulario de registro.html: si el usuario ya existe, si las contraseñas son iguales y que no exceda los parametros establecidos
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
                         validators=[InputRequired(message="Escribe tu nombre"),
                                     Length(min=0, max=30, message="El nombre debe contener maximo 30 caracteres")])

    apellido = StringField('apellido_label',
                           validators=[InputRequired(message="Escribe tu apellido"),
                                       Length(min=0, max=30, message="El apellido debe contener maximo 30 caracteres")])

    edad = StringField('edad_label',
                       validators=[InputRequired(message="Escribe tu edad"),
                                   Length(min=0, max=2, message="La edad debe contener maximo 2 numeros")])

    genero = StringField('genero_label',
                         validators=[InputRequired(message="Escribe tu genero"),
                                     Length(min=0, max=1, message="El género debe ser una sola letra")])

    boton_registro = SubmitField('Registrarse')

    # Metodo que valida si el usuario ya existe en la BD antes de registrarlo
    def validate_usuario(self, usuario):
        user_object = User.query.filter_by(usuario=usuario.data).first()
        if user_object:
            raise ValidationError(
                "El usuario ya existe. Elige otro nombre de usuario")

    # Metodo par avalidar la edad en numeros
    def validate_edad(self, edad):
        #numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        age = int(edad.data)
        if not age < 100:
            print("\n\n", age)
            raise ValidationError("La edad debe ser un número")

    # Metodo para validar el genero del usuario
    def validate_genero(self, genero):
        # user_object = User.query.filter_by(usuario=usuario.data).first()
        generos_restriccion = ["F", "M", "O", "f", "m", "o"]
        if genero.data in generos_restriccion:
            pass
        else:
            raise ValidationError(
                "Escribe (F) para femenino, (M) para masculino y (O) para otro", genero)


# Clase que recibe lo digitado en el index.html y llama la funcion validarUsuario para validar lo recibido
class InicioSesion(FlaskForm):

    usuario = StringField('usuario_label',
                          validators=[InputRequired(message="Usuario requerido")])

    contrasena = PasswordField('contrasena_label',
                               validators=[InputRequired(message="Contraseña requerida"),
                                           validarUsuario])

    boton_inicio = SubmitField('Iniciar Sesión')


# Clase para eliminar una sala
class EliminarSala(FlaskForm):

    input_eliminar_sala = StringField('sala_label')

    boton_eliminar_sala = SubmitField('Eliminar sala')
