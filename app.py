import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'flask-auth-api'}), 200

    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is missing'}), 401

    return app


if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
