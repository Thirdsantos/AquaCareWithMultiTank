from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Import blueprints properly
 

    
    # Import blueprints
    from .routes import sensor_routes, ai
    
    # Register blueprints
    app.register_blueprint(sensor_routes.bp)
    app.register_blueprint(ai.bp)

    
    # Initialize scheduler
   
    
    return app


