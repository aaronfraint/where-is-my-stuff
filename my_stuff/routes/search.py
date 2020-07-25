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

from my_stuff.forms.search_form import SearchForm


# Blueprint Configuration
search_bp = Blueprint(
    'search_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@search_bp.route('/search', methods=['POST'])
@login_required
def search():

    # spaces, containers, items = None, None, None

    form = SearchForm()

    search_txt = form.search_txt.data

    # Get all SPACES for this user
    spaces = Space.query.join(Space.users).filter_by(id=current_user.id).all()

    # See if any space matches this search text
    selected_space = None
    for space in spaces:
        if space.name.lower() == search_txt.lower():
            selected_space = space

    # See if any containers have this name
    space_id_list = [s.uid for s in spaces]
    all_containers = Container.query.filter(Container.space_id.in_(space_id_list)).all()

    selected_containers = []
    for container in all_containers:
        if container.name.lower() == search_txt.lower():
            selected_containers.append(container)

    if len(selected_containers) == 0:
        selected_containers = None

    # See if any tags match this search
    search_txt_as_tag = search_txt.replace(" ", "-").lower()

    tag = Tag.query.filter_by(
        name=search_txt_as_tag
    ).first()

    # If there's a matching tag, get all items with that tag
    if tag:
        items = Item.query.join(Item.tags).filter_by(name=search_txt_as_tag).all()
    else:
        items = None

    return render_template(
        'search.html',
        make_random_gradient=make_random_gradient,
        search_txt=search_txt,
        selected_space=selected_space,
        selected_containers=selected_containers,
        tag=tag,
        search_form=SearchForm(),
        items=items,
        # containers=containers,
    )
