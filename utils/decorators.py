from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """
    Decorador para proteger rutas que requieren autenticación.
    Redirige al login si el usuario no está autenticado.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function