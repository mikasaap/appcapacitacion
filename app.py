import os
from flask import Flask, url_for, redirect
from config import config
from models.database import init_db

# Crear la aplicación Flask
app = Flask(__name__, template_folder='views')

# Cargar configuración según el entorno
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])
app.secret_key = app.config['SECRET_KEY']

# Inicializar la base de datos  
init_db()

# Registrar blueprints
from controllers.auth_controller import auth_bp
app.register_blueprint(auth_bp)

from controllers.dashboard_controller import dashboard_bp
app.register_blueprint(dashboard_bp)

from controllers.estudiantes_controller import estudiantes_bp
app.register_blueprint(estudiantes_bp)

from controllers.cursos_controller import cursos_bp
app.register_blueprint(cursos_bp)

from controllers.inscripciones_controller import inscripciones_bp
app.register_blueprint(inscripciones_bp)

from controllers.usuario_controller import usuario_bp
app.register_blueprint(usuario_bp)

# Ruta principal
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])