from flask import Blueprint, render_template, request, redirect, url_for, flash 
from models.database import get_db_connection
inscripciones_bp = Blueprint('inscripciones', __name__, 
                             template_folder='../views/inscripciones', url_prefix='/inscripciones')

@inscripciones_bp.route('/')
def view_inscripciones():
    conn = get_db_connection()
    inscripciones = conn.execute("""
        SELECT i.id, i.fecha, c.descripcion AS curso, e.nombre || ' ' || e.apellidos AS estudiante
        FROM inscripciones i
        JOIN cursos c ON i.curso_id = c.id
        JOIN estudiantes e ON i.estudiante_id = e.id
    """).fetchall()
    conn.close()
    return render_template('inscripciones.html', inscripciones=inscripciones)
@inscripciones_bp.route('/new', methods=('GET', 'POST'))
def create_inscripcion():
    conn = get_db_connection()
    cursos = conn.execute('SELECT * FROM cursos').fetchall()
    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    if request.method == 'POST':
        fecha = request.form['fecha']
        curso_id = request.form['curso_id']
        estudiante_id = request.form['estudiante_id']
        conn.execute('INSERT INTO inscripciones (fecha, curso_id, estudiante_id) VALUES (?, ?, ?)',
                     (fecha, curso_id, estudiante_id))
        conn.commit()
        conn.close()
        return redirect(url_for('inscripciones.view_inscripciones'))
    conn.close()
    return render_template('forminscripcion.html', cursos=cursos, estudiantes=estudiantes)
@inscripciones_bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_inscripcion(id):
    conn = get_db_connection()
    inscripcion = conn.execute('SELECT * FROM inscripciones WHERE id = ?', (id,)).fetchone()
    cursos = conn.execute('SELECT * FROM cursos').fetchall()
    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    if request.method == 'POST':
        fecha = request.form['fecha']
        curso_id = request.form['curso_id']
        estudiante_id = request.form['estudiante_id']
        conn.execute('UPDATE inscripciones SET fecha = ?, curso_id = ?, estudiante_id = ? WHERE id = ?',
                     (fecha, curso_id, estudiante_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('inscripciones.view_inscripciones'))
    conn.close()
    return render_template('newforminscripcion.html', inscripcion=inscripcion, 
                           cursos=cursos, estudiantes=estudiantes)

@inscripciones_bp.route('/delete/<int:id>')
def delete_inscripcion(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM inscripciones WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Inscripción eliminada correctamente.')
    return redirect(url_for('inscripciones.view_inscripciones'))