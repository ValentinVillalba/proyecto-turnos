import mysql.connector
from mysql.connector import Error
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
        print("DESCONECTADO DE MYSQL")

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turnos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL
            );
        """)
        connection.commit()
        print("TABLA CREADA")
    except Error as e:
        print(f"ERROR AL CREAR LA TABLA: {e}")