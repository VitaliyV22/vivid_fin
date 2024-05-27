from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config


db = SQLAlchemy()
login = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)
    csrf.init_app(app)
    
    from .routes import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')
    
    return app
