from flask import Flask,current_app
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .auth import aut
   
    app.register_blueprint(aut, url_prefix='/')
    
    
    return app

