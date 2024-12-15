from flask import Flask
from config.config import config
from app.api.routes import api_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Register blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app