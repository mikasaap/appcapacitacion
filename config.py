import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///academia.db'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'production'
    
    # Extraer el nombre de archivo de la base de datos SQLite
    @property
    def DATABASE(self):
        if self.DATABASE_URL.startswith('sqlite:///'):
            return self.DATABASE_URL.replace('sqlite:///', '')
        return 'academia.db'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    FLASK_ENV = 'production'

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}