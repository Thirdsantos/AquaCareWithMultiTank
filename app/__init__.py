from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Import blueprints properly
    from .routes import sensor_routes, ai
    
    # Register blueprints
    #app.register_blueprint(ai.bp)            # Assuming ai.py defines bp Blueprint
    app.register_blueprint(sensor_routes.bp) # Assuming sensor_routes.py defines bp Blueprint
  
    
    return app


