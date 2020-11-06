from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Usuario(db.Model):

    __nombreTabla__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    usuario = db.Column(db.String(25), unique=True, nullable=False)
    contraseña = db.Column(db.String(), nullable=False)
    edad = db.Column(db.String(2), nullable=False)
    genero = db.Column(db.String(1), nullable=False)


    db.create_all()
