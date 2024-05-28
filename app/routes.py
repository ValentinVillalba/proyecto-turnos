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
    
