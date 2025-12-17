from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from config import Config
import os

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.url_map.strict_slashes = False
    
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
        "https://your-app-name.vercel.app"
    ]
    
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": True
        }
    })
    
    instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    
    db.init_app(app)
    ma.init_app(app)
    
    from app.blueprints.users import users_bp
    from app.blueprints.messages import messages_bp
    from app.blueprints.rooms import rooms_bp
    
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(rooms_bp, url_prefix='/api/rooms')
    
    with app.app_context():
        db.create_all()
    
    return app