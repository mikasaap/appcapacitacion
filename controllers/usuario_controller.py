from flask import Blueprint, request, url_for, redirect, render_template, flash, session
from models.database import get_db_connection

usuario_bp = Blueprint('usuario', __name__, 
                           template_folder='../views/usuarios', url_prefix='/usuario')
@usuario_bp.route('/')
def view_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)