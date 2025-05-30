from flask import Flask
from flask_apscheduler import APScheduler

def create_app():
    app = Flask(__name__)
    
    # Import blueprints properly
    from .routes import sensor_routes

    
    # Import blueprints
    from .routes import sensor_routes, ai
    
    # Register blueprints
    app.register_blueprint(sensor_routes.bp)
    #app.register_blueprint(ai.bp)  # Uncomment when ai blueprint is ready
    
    # Initialize scheduler
   
    
    return app


