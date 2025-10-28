from flask import Blueprint, request, url_for, redirect, render_template, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db_connection
import sqlite3
auth_bp = Blueprint('auth', __name__, template_folder='../views/auth', url_prefix='/auth')

@auth_bp.route('/login', methods=('GET', 'POST'))   
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']  #El pasword de prueba es admin742##
        conn= get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ?', (user,)).fetchone()
        if user and check_password_hash(user['password'], password):
            return redirect(url_for('dashboard.index'))
        else:
            flash('Usuario o contraseña incorrectos.')
            print('Fallo de autenticación para el usuario:', request.form['username'])
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        celular = request.form['phone']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            print('Error de registro: las contraseñas no coinciden para el usuario:', username)
            return render_template('auth/register.html')
        conn = get_db_connection()
        try:
            hashed_password = generate_password_hash(password)
            conn.execute('INSERT INTO usuarios (username, email, password, celular) VALUES (?, ?, ?, ?)',
                            (username, email, hashed_password, celular))
            conn.commit()
            conn.close()
            flash('Usuario registrado correctamente.', 'success')
            print('Nuevo usuario registrado:', username)
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario o correo electrónico ya existe.', 'danger')
        finally:
            conn.close()
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.','info')
    return redirect(url_for('auth.login'))