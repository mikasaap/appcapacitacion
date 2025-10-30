from flask import Blueprint, request, url_for, redirect, render_template, flash, session
from models.database import get_db_connection
from utils.decorators import login_required

cursos_bp = Blueprint('cursos', __name__, 
                           template_folder='../views/cursos', url_prefix='/cursos')

@cursos_bp.route('/')
@login_required
def view_cursos():
    conn = get_db_connection()
    cursos = conn.execute('SELECT * FROM cursos').fetchall()
    conn.close()
    return render_template('cursos.html', cursos=cursos)
@cursos_bp.route('/new', methods=('GET', 'POST'))
@login_required
def create_curso():
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            horas = request.form['horas']
            conn = get_db_connection()
            conn.execute('INSERT INTO cursos (descripcion, horas) VALUES (?, ?)',
                        (descripcion, horas))
            conn.commit()
            conn.close()
            return redirect(url_for('cursos.view_cursos'))
        return render_template('formcurso.html')

@cursos_bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit_curso(id):
    conn = get_db_connection()
    curso = conn.execute('SELECT * FROM cursos WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        horas = request.form['horas']
        conn.execute('UPDATE cursos SET descripcion = ?, horas = ? WHERE id = ?',
                     (descripcion, horas, id))
        conn.commit()
        conn.close()
        return redirect(url_for('cursos.view_cursos'))
    conn.close()
    return render_template('formcurso.html', curso=curso)
@cursos_bp.route('/delete/<int:id>')
@login_required
def delete_curso(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cursos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Curso eliminado correctamente.')
    return redirect(url_for('cursos.view_cursos'))
