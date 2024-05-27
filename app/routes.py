from flask import jsonify, render_template
from app import app
from app.models import *

#RUTAS

@app.route('/')
def index():
    return render_template('index.html')

# Ruta para obtener todos los datos de la tabla turnos en el front-end
@app.route('/get_data_turnos')
def get_data():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM turnos")
        rows = cursor.fetchall()
        close_connection(connection)
        return jsonify(rows)
    else:
        return jsonify([])

#Ruta para crear una tabla, no se usa desde el front-end
@app.route('/create_table')
def create_table_route():
    connection = create_connection()
    if connection:
        create_table(connection)
        close_connection(connection)
        return "TABLA CREADA"
    else:
        return "ERROR AL CONECTAR A MYSQL"