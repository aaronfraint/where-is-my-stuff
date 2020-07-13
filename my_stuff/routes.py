"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import current_user, login_required, logout_user
from .models import Space, db, User, ContainerCategory, Container, ContainerCategory
from .forms import SpaceForm, CategoryForm, ContainerForm

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


@main_bp.route('/spaces', methods=['GET'])
@login_required
def spaces():
    """Logged-in User Dashboard."""
    user = User.query.filter_by(username=current_user.username).first()
    spaces = Space.query.filter_by(user_id=user.id).all()

    return render_template(
        'spaces.html',
        spaces=spaces,
        form=SpaceForm(),
    )

@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))


@main_bp.route('/add/space', methods=['GET', 'POST'])
@login_required
def add_space():
    """
    """
    form = SpaceForm()

    return render_template(
        'add_space.html',
        form=form,
    )
    

@main_bp.route('/save/space', methods=['GET', 'POST'])
@login_required
def save_space():
    """
    """

    form = SpaceForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        space = Space(name=form.name.data, description=form.description.data, user_id=user.id)
        db.session.add(space)
        db.session.commit()
        return redirect(url_for('main_bp.spaces'))

    return render_template(
        'add_space.html',
        form=form,
    )
    


@main_bp.route('/space/<space_id>', methods=['GET', 'POST'])  # /landingpage/A
@login_required
def space_by_id(space_id):
    space = Space.query.filter_by(uid=space_id).first()

    containers = Container.query.filter_by(space_id=space_id).all()

    cateogry_form = CategoryForm()
    container_form = ContainerForm()

    return render_template(
        'single_space.html',
        space=space,
        category_form=cateogry_form,
        container_form=container_form,
        containers=containers,
    )
    


@main_bp.route('/space/<space_id>/add/category', methods=['POST'])
@login_required
def add_category_to_space(space_id):
    space = Space.query.filter_by(uid=space_id).first()
    container_form = ContainerForm()
    category_form = CategoryForm()

    if request.method == 'POST':
        if category_form.validate_on_submit() and category_form.validate_on_submit():

            payload = category_form.category_name.data

            # See if it's already in the table
            category = ContainerCategory.query.filter_by(space_id=space_id, name=payload).all()
            if category:
                flash(f"{payload} already exists", "warning")
                return redirect(url_for('main_bp.space_by_id', space_id=space_id))

            else:
                category = ContainerCategory(name=payload, space_id=space_id)
                db.session.add(category)
                db.session.commit()
                flash(f"Added new category: {payload}", "success")
                return redirect(url_for('main_bp.space_by_id', space_id=space_id))



        # if container_form.validate_on_submit() and container_form.category.data and container_form.container_name.data:
        #     category = ContainerCategory.query.filter_by(name=container_form.category.data).first()
        #     container = Container(name=container_form.container_name.data, space_id=space_id, category_id=category.uid)

        #     db.session.add(container)
        #     db.session.commit()
        #     return redirect(url_for('main_bp.space_by_id', space_id=space_id))

    return render_template(
        'single_space.html',
        space=space,
        category_form=category_form,
        container_form=container_form
    )
    

@main_bp.route('/space/<space_id>/add/container', methods=['POST'])
@login_required
def add_container_to_space(space_id):
    space = Space.query.filter_by(uid=space_id).first()
    container_form = ContainerForm()
    category_form = CategoryForm()

    if request.method == 'POST':

        if container_form.validate_on_submit() and container_form.category.data and container_form.container_name.data:
            category = ContainerCategory.query.filter_by(name=container_form.category.data).first()
            container = Container(name=container_form.container_name.data, space_id=space_id, category_id=category.uid)

            db.session.add(container)
            db.session.commit()

            return redirect(url_for('main_bp.space_by_id', space_id=space_id))

    return render_template(
        'single_space.html',
        space=space,
        category_form=category_form,
        container_form=container_form
    )
    