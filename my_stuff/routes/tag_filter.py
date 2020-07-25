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
tag_bp = Blueprint(
    'tag_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@tag_bp.route('/tagged/<tag_slug>', methods=['GET'])
@login_required
def tags(tag_slug):

    # Get all items that have this slug,
    # from all spaces that belong to this user

    all_spaces = Space.query.all()
    spaces = [s for s in all_spaces if current_user in s.users]

    selected_items = []

    for space in spaces:
        for container in space.containers:
            for item in container.items:
                tags = [t.slug() for t in item.tags]
                if tag_slug in tags:
                    selected_items.append(
                        [space, container, item]
                    )


    return render_template(
        'tags.html',
        tag_slug=tag_slug,
        spaces=spaces,
        make_random_gradient=make_random_gradient,
        selected_items=selected_items,
        search_form=SearchForm()
    )

