from models.database import init_db
from flask import Flask, url_for, redirect, session

init_db()
app = Flask(__name__, template_folder='views')
app.secret_key = 'your_secret_key'

from controllers.auth_controller import auth_bp
app.register_blueprint(auth_bp)
@app.route('/')
def index():
    return redirect(url_for('auth.login'))
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
if __name__ == '__main__':
    #init_db()
    #insertar_bd()
    app.run(debug=True)
