from flask import jsonify, render_template
from app.models import create_connection, close_connection
from app import app

#TODO: Revisar el tema del Blueprint

#RUTAS

# Index
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