"""Main Flask application."""
from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend import db
from backend.routes.task_routes import task_bp
from backend.routes.comment_routes import comment_bp

def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(task_bp, url_prefix='/api/tasks')
    app.register_blueprint(comment_bp, url_prefix='/api/tasks')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

