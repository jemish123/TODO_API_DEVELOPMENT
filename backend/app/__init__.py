from flask import Flask
from app.database.connection import init_db
from app.api.routes import todos_bp


def create_app():
    app = Flask(__name__)
    
    # This will allow the addresses to request data to this API
    init_db()
    
    # Register route blueprints
    app.register_blueprint(todos_bp, url_prefix='/todos')
    return app