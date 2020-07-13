"""Routes for user authentication."""
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user


from my_stuff.forms.forms import LoginForm, SignupForm


from my_stuff.models.user import db, User

from . import login_manager


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route('/getstarted', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('spaces_bp.spaces'))  

    login_form = LoginForm()
    signup_form = SignupForm()

    if request.method == 'POST':

        if request.form['submit'] == 'login':

            # Validate login attempt
            if login_form.validate_on_submit() and login_form.email.data:
                user = User.query.filter_by(email=login_form.email.data).first()
                if user and user.check_password(password=login_form.password.data):
                    login_user(user)
                    return redirect(url_for('spaces_bp.spaces'))

                flash(r'Invalid username/password combination', "danger")

        if request.form['submit'] == 'signup':

            if signup_form.validate_on_submit() and signup_form.email.data:
                existing_user = User.query.filter_by(email=signup_form.email.data).first()
                if existing_user is None:
                    user = User(
                        username=signup_form.username.data,
                        email=signup_form.email.data
                    )
                    user.set_password(signup_form.password.data)
                    db.session.add(user)
                    db.session.commit()  # Create new user
                    login_user(user)  # Log in as newly created user
                    return redirect(url_for('spaces_bp.spaces'))

                flash('A user already exists with that email address.', "danger")

    return render_template(
        'get_started.html',
        login_form=login_form,
        signup_form=signup_form,
    )
    
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """

    return render_template(
        'sign_up.html',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))
