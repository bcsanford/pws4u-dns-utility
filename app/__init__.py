import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Load .env file for DB credentials and secrets
load_dotenv()

# Flask app instance
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

# Database configuration
db_user = os.getenv("DB_USER", "pws4u")
db_pass = os.getenv("DB_PASS", "")
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "pws4u")

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "Please log in to access this page."

# Register blueprints
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# Import models for Flask-Login user loader
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
