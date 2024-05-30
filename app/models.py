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
class TablaTurnos(db.Model):
    __tablename__ = 'tabla_turnos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)