from flask import Blueprint, render_template, session
from utils.decorators import login_required

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../views/dashboard', url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    # Pasar información del usuario al template
    return render_template('dashboard/index.html', username=session.get('username'))