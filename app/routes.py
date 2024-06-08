from datetime import date, time, timedelta
from flask import jsonify, render_template
from app.models import create_connection, close_connection
from app import app

#TODO: Revisar el tema del Blueprint

#Serializar los datos de la base de datos
def serialize_data(rows):
    for row in rows:
        for key, value in row.items():
            if isinstance(value, (timedelta, date, time)):
                row[key] = str(value)
    return rows

#RUTAS

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Login
@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para obtener todos los datos de la tabla turnos en el front-end
@app.route('/get_data_turnos')
def get_data():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM turnos")
        rows = cursor.fetchall()
        close_connection(connection)
        rows = serialize_data(rows)
        return jsonify(rows)
    else:
        return jsonify([])