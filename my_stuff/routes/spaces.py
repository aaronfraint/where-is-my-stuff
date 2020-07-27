"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from my_stuff import db, make_random_gradient
from my_stuff.models.all_models import (
    User,
    Space,
    Container,
    ContainerCategory,
    Item,
    Tag
)

from my_stuff.forms.all_spaces_page_form import AddSpaceForm
from my_stuff.forms.single_space_page_form import AddContainerForm
from my_stuff.forms.invite_user_to_space import InviteForm
from my_stuff.forms.search_form import SearchForm


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
    spaces = Space.query.join(Space.users).filter_by(id=current_user.id).all()

    private_spaces = []
    shared_spaces = []

    for space in spaces:
        if space.num_users() == 1:
            private_spaces.append(space)
        else:
            shared_spaces.append(space)

    return render_template(
        'spaces.html',
        private_spaces=private_spaces,
        shared_spaces=shared_spaces,
        form=AddSpaceForm(),
        make_random_gradient=make_random_gradient,
        search_form=SearchForm()
    )


@spaces_bp.route('/save/space', methods=['POST'])
@login_required
def save_space():
    """Add a space"""

    form = AddSpaceForm()

    if form.validate_on_submit():

        space_name = form.space_name.data.lstrip().rstrip()
        space_desc = form.description.data.lstrip().rstrip()

        # user = User.query.filter_by(name=current_user.name).first()
        # space = Space.query.filter_by(
        #     user_id=user.id,
        #     name=space_name,
        # ).first()

        space = Space.query.filter_by(
            name=space_name
        ).join(Space.users).filter_by(id=current_user.id).first()

        if space:
            flash(f"Space '{space.name}' already exists. Use a different name.", "danger")

        else:
            space = Space(
                name=space_name,
                description=space_desc,
                users=[current_user]
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

    containers = Container.query.filter_by(
        space_id=space_id
    ).order_by(Container.name).all()

    all_item_tags = []

    for container in containers:
        for tag in container.tags():
            if tag not in all_item_tags:
                all_item_tags.append(tag)

    if len(all_item_tags) == 0:
        all_item_tags = None

    form = AddContainerForm()

    return render_template(
        'single_space.html',
        space=space,
        form=form,
        containers=containers,
        make_random_gradient=make_random_gradient,
        all_item_tags=all_item_tags,
        invite_form=InviteForm(),
        search_form=SearchForm(),
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

    return redirect(url_for('container_bp.container_by_id', container_id=container.uid))


@spaces_bp.route('/space/<space_id>/invite', methods=['POST'])
@login_required
def invite_user_to_space(space_id):
    form = InviteForm()

    if form.validate_on_submit():
        space = Space.query.filter_by(uid=space_id).first()

        new_user = User.query.filter_by(email=form.invite_email.data).first()

        if not new_user:
            flash("This user does not exist", "danger")
            return redirect(url_for('spaces_bp.space_by_id', space_id=space_id))

        else:
            space.users.append(new_user)
            db.session.commit()
            flash(f"Invited: {form.invite_email.data}", "success")

    else:
        for error in form.invite_email.errors:
            flash(error, "danger")

    return redirect(url_for('spaces_bp.space_by_id', space_id=space_id))
    