"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user


# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/', methods=['GET'])
def home():
    """Landing page."""
    return render_template('home.html',
                           title="Where's my stuff?",
                           description="Landing page")


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
