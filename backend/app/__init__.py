import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate

# Initialize SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configure the application
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize API
    api = Api(app)
    
    # Register blueprints and resources
    from app.api.paddock import PaddockResource, PaddockListResource
    from app.api.ndvi import NDVIResource
    from app.api.weather import WeatherResource
    
    # Add API resources
    api.add_resource(PaddockListResource, '/api/paddocks')
    api.add_resource(PaddockResource, '/api/paddocks/<uuid:paddock_id>')
    api.add_resource(NDVIResource, '/api/paddocks/<uuid:paddock_id>/ndvi')
    api.add_resource(WeatherResource, '/api/weather')
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app 