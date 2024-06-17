from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="159870",
    database="bdd_turnos"
)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        # Verificar el rol y redirigir según el rol
        if user['rol'] == 'secretaria':
            return redirect(url_for('secretaria_dashboard'))
        elif user['rol'] == 'cliente':
            return redirect(url_for('cliente_dashboard'))
    else:
        flash('Usuario o contraseña incorrecta, ingrese los datos nuevamente')
        return redirect(url_for('login'))

@app.route('/secretaria_dashboard')
def secretaria_dashboard():
    return render_template('index1.html')

@app.route('/cliente_dashboard')
def cliente_dashboard():
    return "Bienvenido, Cliente"

if __name__ == '__main__':
    app.run(debug=True)
