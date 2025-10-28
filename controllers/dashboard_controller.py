from flask import Blueprint, render_template
#from flask_login import login_required
dashboard_bp = Blueprint('dashboard', __name__, template_folder='../views/dashboard', url_prefix='/dashboard')

@dashboard_bp.route('/')
#@login_required
def index():
    return render_template('dashboard/index.html')