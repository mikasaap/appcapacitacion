import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_muy_segura'
    DATABASE = "academia.db"
