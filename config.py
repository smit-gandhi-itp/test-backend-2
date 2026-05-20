import os
from datetime import timedelta


class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-please-change')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    # In production, ensure SECRET_KEY and JWT_SECRET_KEY are set via environment


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
