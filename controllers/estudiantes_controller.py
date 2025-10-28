from flask import Blueprint, request, url_for, redirect, render_template, flash, session
from models.database import get_db_connection

estudiantes_bp = Blueprint('estudiantes', __name__, 
                           template_folder='../views/estudiantes', url_prefix='/estudiantes')
@estudiantes_bp.route('/')
def view_estudiantes():
    conn = get_db_connection()
    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    conn.close()
    return render_template('estudiantes.html', estudiantes=estudiantes)
@estudiantes_bp.route('/new', methods=('GET', 'POST'))
def create_estudiante():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        conn = get_db_connection()
        conn.execute('INSERT INTO estudiantes (nombre, apellidos, fecha_nacimiento) VALUES (?, ?, ?)',
                        (nombre, apellidos, fecha_nacimiento))
        conn.commit()
        conn.close()
        return redirect(url_for('estudiantes.view_estudiantes'))

    return render_template('formestudiante.html')
@estudiantes_bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_estudiante(id):
    conn = get_db_connection()
    estudiante = conn.execute('SELECT * FROM estudiantes WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        conn.execute('UPDATE estudiantes SET nombre = ?, apellidos = ?, fecha_nacimiento = ? WHERE id = ?',
                     (nombre, apellidos, fecha_nacimiento, id))
        conn.commit()
        conn.close()
        return redirect(url_for('estudiantes.view_estudiantes'))
    conn.close()
    return render_template('formestudiante.html', estudiante=estudiante)
@estudiantes_bp.route('/delete/<int:id>')
def delete_estudiante(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM estudiantes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Estudiante eliminado correctamente.')
    return redirect(url_for('estudiantes.view_estudiantes')) 
