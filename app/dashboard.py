from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import AssessmentResult

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    return render_template('landing.html')


@dashboard_bp.route('/dashboard')
@login_required
def home():
    results = AssessmentResult.query.filter_by(
        user_id=current_user.id
    ).order_by(AssessmentResult.created_at.desc()).all()
    return render_template('dashboard.html', user=current_user, results=results)