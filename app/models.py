import mysql.connector
from mysql.connector import Error
from app import db
import json

with open('password.json') as pass_file:
    pass_data = json.load(pass_file)

secret_pass = pass_data['password']

#FUNCIONES

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='bdd_turnos',
            user='root',
            password=secret_pass
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"ERROR AL CONECTAR A MYSQL: {e}")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MYSQL DESCONECTADO CORRECTAMENTE")

#TABLAS
class Pacientes(db.Model):
    __tablename__ = 'pacientes'
    id_paciente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    fecha_nac = db.Column(db.Date, nullable=False)
    obra_soc = db.Column(db.String(30), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    direccion = db.Column(db.String(30), nullable=False)

class Turnos(db.Model):
    __tablename__ = 'turnos'
    id_turno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_usuario = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    rol = db.Column(db.Enum('secretaria', 'cliente'), nullable=False)
    obra_soc = db.Column(db.String(30), nullable=True)