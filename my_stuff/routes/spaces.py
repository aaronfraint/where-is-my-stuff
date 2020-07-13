"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from my_stuff.models.container import Container, ContainerCategory
from my_stuff.models.space import Space
from my_stuff.models.user import User
from my_stuff import db

from my_stuff.forms.all_spaces_page_form import AddSpaceForm
from my_stuff.forms.single_space_page_form import AddContainerForm


# Blueprint Configuration
spaces_bp = Blueprint(
    'spaces_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@spaces_bp.route('/spaces', methods=['GET'])
@login_required
def spaces():
    """Logged-in User landing page"""
    user = User.query.filter_by(username=current_user.username).first()
    spaces = Space.query.filter_by(user_id=user.id).all()

    return render_template(
        'spaces.html',
        spaces=spaces,
        form=AddSpaceForm(),
    )


@spaces_bp.route('/save/space', methods=['POST'])
@login_required
def save_space():
    """Add a space"""

    form = AddSpaceForm()

    if form.validate_on_submit():

        space_name = form.space_name.data.lstrip().rstrip()
        space_desc = form.description.data

        # Make sure it's not empty text
        if len(space_name.replace(" ", "")) == 0:
            flash(f"Space name can't only be spaces", "danger")
            return redirect(url_for('spaces_bp.spaces'))

        # Same for the description
        if len(space_desc.replace(" ", "")) == 0:
            flash(f"Please add a description for your space", "danger")
            return redirect(url_for('spaces_bp.spaces'))

        user = User.query.filter_by(username=current_user.username).first()
        space = Space.query.filter_by(
            user_id=user.id,
            name=space_name,
        ).first()

        if space:
            flash(f"Space '{space.name}' already exists. Use a different name.", "danger")

        else:
            space = Space(
                name=space_name,
                description=space_desc,
                user_id=user.id
            )

            db.session.add(space)
            db.session.commit()
            flash(f"+ Space '{space.name}'", "success")

    else:
        for error in form.space_name.errors:
            flash(error, "danger")
        for error in form.description.errors:
            flash(error, "danger")

    return redirect(url_for('spaces_bp.spaces'))


@spaces_bp.route('/space/<space_id>', methods=['GET', 'POST'])  # /landingpage/A
@login_required
def space_by_id(space_id):
    """Page for a single space, including:
        - form to add new containers
        - list of items in each container
    """
    space = Space.query.filter_by(uid=space_id).first()

    containers = Container.query.filter_by(space_id=space_id).all()

    form = AddContainerForm()

    return render_template(
        'single_space.html',
        space=space,
        form=form,
        containers=containers,
    )


@spaces_bp.route('/space/<space_id>/add/container', methods=['POST'])
@login_required
def add_container_to_space(space_id):
    form = AddContainerForm()

    if form.validate_on_submit():

        # Try to query this container. If it exists, warn the user and abort!
        container_exists = Container.query.filter_by(
            name=form.container_name.data,
            space_id=space_id
        ).first()

        if container_exists:
            flash(f"Container '{form.container_name.data}' already exists. Aborting.", "danger")
            return redirect(url_for('spaces_bp.space_by_id', space_id=space_id))

        # If neither category is provided...
        if not form.new_category.data and not form.existing_category.data:
            flash("Please provide a new category or select an existing category.", "danger")
            return redirect(url_for('spaces_bp.space_by_id', space_id=space_id))

        # Use manually typed category if both are provided...
        if form.new_category.data and form.existing_category.data:
            cat_name = form.new_category.data
            # flash("Both categories provided, using manual one", "info")

        # Use the dropdown category if it's the only one
        elif form.existing_category.data and not form.new_category.data:
            cat_name = form.existing_category.data
            # flash("Using the dropdown category", "info")

        # Use the new category if it's the only one
        elif form.new_category.data and not form.existing_category.data:
            cat_name = form.new_category.data
            # flash("Using a new category", "info")

        # Query the category. Make it if it doesn't exist
        # -----------------------------------------------

        category = ContainerCategory.query.filter_by(
            name=cat_name,
            space_id=space_id
        ).first()

        if not category:
            category = ContainerCategory(
                name=cat_name,
                space_id=space_id
            )

            db.session.add(category)
            db.session.commit()
            flash(f"+ category: {cat_name}", "success")

        # Add the new container
        # ---------------------

        container = Container(
            name=form.container_name.data,
            space_id=space_id,
            category_id=category.uid
        )
        db.session.add(container)
        db.session.commit()
        flash(f"+ container: {container.name}", "success")

    else:
        for error in form.container_name.errors:
            flash(error, "danger")
        for error in form.new_category.errors:
            flash(error, "danger")
        for error in form.existing_category.errors:
            flash(error, "danger")

    return redirect(url_for('spaces_bp.space_by_id', space_id=space_id))
    