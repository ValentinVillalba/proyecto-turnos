from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

app = Flask(__name__)

with open('password.json') as pass_file:
    pass_data = json.load(pass_file)

secret_pass = pass_data['password']

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:'+ secret_pass +'@localhost/bdd_turnos'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models