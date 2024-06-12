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
    
    from .routes import main_bp
    from .user_routes import user_bp
    from .transaction_routes import transaction_bp
    from .budget_routes import budget_bp
    from .savings_goal_routes import savings_goal_bp
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    app.register_blueprint(budget_bp, url_prefix='/budgets')
    app.register_blueprint(savings_goal_bp, url_prefix='/savings_goals')
    
    return app
