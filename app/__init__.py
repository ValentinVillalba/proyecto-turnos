from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

with open('password.json') as pass_file:
    pass_data = json.load(pass_file)

secret_pass = pass_data['password']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:'+ secret_pass +'@localhost/bdd_turnos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#TABLAS CREADAS
class Turnos(db.Model):
    __tablename__ = 'turnos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

from app import routes, models
