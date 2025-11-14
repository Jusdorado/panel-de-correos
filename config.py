import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración de la aplicación Mundosol"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-prod')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://panel_user:panel_pass_123@127.0.0.1/panel_correos')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook')
    WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN', 'change-me')
