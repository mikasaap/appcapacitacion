from flask import Blueprint, request, url_for, redirect, render_template, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db_connection
import sqlite3

auth_bp = Blueprint('auth', __name__, template_folder='../views/auth', url_prefix='/auth')

@auth_bp.route('/login', methods=('GET', 'POST'))   
def login():
    # Si ya está autenticado, redirigir al dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            # Guardar información del usuario en la sesión
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        celular = request.form['phone']
        confirm_password = request.form['confirm_password']
        
        # Validar que las contraseñas coincidan
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('auth/register.html')
        
        conn = get_db_connection()
        try:
            hashed_password = generate_password_hash(password)
            conn.execute('INSERT INTO usuarios (username, email, password, celular) VALUES (?, ?, ?, ?)',
                        (username, email, hashed_password, celular))
            conn.commit()
            flash('Usuario registrado correctamente. Por favor inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario o correo electrónico ya existe.', 'danger')
        finally:
            conn.close()
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))