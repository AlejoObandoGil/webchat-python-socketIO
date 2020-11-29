# Modelo de la palicacion para crear la BD SQLPostgres  de Heroku con SQLAlchemy 

# Librerias
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# trabajaremos con el gestor sqlAlchemy
db = SQLAlchemy()


# Esta clase modelo crea la tabla en heroku-postgres
class User(UserMixin, db.Model):

    __tablename__ = 'usuarios2'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(25), unique=True, nullable=False)
    contrasena = db.Column(db.String(), nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    edad = db.Column(db.String(2), nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    

'''
CREATE TABLE usuarios( id SERIAL PRIMARY KEY, usuario VARCHAR(25) UNIQUE NOT NULL, contraseña TEXT NOT NULL, nombre VARCHAR(30) NOT NULL, apellido VARCHAR(30) NOT NULL, edad VARCHAR(2) NOT NULL, genero VARCHAR(1) NOT NULL);
'''