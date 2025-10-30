from flask import Blueprint, request, url_for, redirect, render_template, flash
from models.database import get_db_connection
from utils.decorators import login_required

estudiantes_bp = Blueprint('estudiantes', __name__, 
                           template_folder='../views/estudiantes', url_prefix='/estudiantes')

@estudiantes_bp.route('/')
@login_required
def view_estudiantes():
    conn = get_db_connection()
    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    conn.close()
    return render_template('estudiantes.html', estudiantes=estudiantes)

@estudiantes_bp.route('/new', methods=('GET', 'POST'))
@login_required
def create_estudiante():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO estudiantes (nombre, apellidos, fecha_nacimiento) VALUES (?, ?, ?)',
                        (nombre, apellidos, fecha_nacimiento))
            conn.commit()
            flash('Estudiante creado correctamente.', 'success')
        except Exception as e:
            flash(f'Error al crear estudiante: {str(e)}', 'danger')
        finally:
            conn.close()
        
        return redirect(url_for('estudiantes.view_estudiantes'))
    
    return render_template('formestudiante.html')

@estudiantes_bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit_estudiante(id):
    conn = get_db_connection()
    estudiante = conn.execute('SELECT * FROM estudiantes WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        
        try:
            conn.execute('UPDATE estudiantes SET nombre = ?, apellidos = ?, fecha_nacimiento = ? WHERE id = ?',
                        (nombre, apellidos, fecha_nacimiento, id))
            conn.commit()
            flash('Estudiante actualizado correctamente.', 'success')
        except Exception as e:
            flash(f'Error al actualizar estudiante: {str(e)}', 'danger')
        finally:
            conn.close()
        
        return redirect(url_for('estudiantes.view_estudiantes'))
    
    conn.close()
    return render_template('formestudiante.html', estudiante=estudiante)

@estudiantes_bp.route('/delete/<int:id>')
@login_required
def delete_estudiante(id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM estudiantes WHERE id = ?', (id,))
        conn.commit()
        flash('Estudiante eliminado correctamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar estudiante: {str(e)}', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('estudiantes.view_estudiantes'))
