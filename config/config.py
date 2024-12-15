import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    VECTOR_DB_PATH = BASE_DIR / 'VectorDB'
    ASSETS_PATH = BASE_DIR / 'assets'
    
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5001
    
    # Add other configuration variables as needed
    MODEL_CACHE_DIR = str(Path.home() / '.cache' / 'huggingface')
    DEFAULT_MODEL = "llama3.1"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}