import os

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_change_in_production')
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
    
    # Database configuration
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'smartfarm')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'dev_password')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'smartfarm')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Agromonitoring API configuration
    AGROMONITORING_API_KEY = os.environ.get('AGROMONITORING_API_KEY')
    AGROMONITORING_API_URL = 'https://api.agromonitoring.com/agro/1.0' 