from flask import Blueprint, render_template, redirect, url_for, flash, request
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

from my_stuff.forms.single_container_page_form import AddItemForm
from my_stuff.forms.search_form import SearchForm

# Blueprint Configuration
container_bp = Blueprint(
    'container_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@container_bp.route('/container/<container_id>', methods=['GET'])
@login_required
def container_by_id(container_id):
    """Page for a single container, including:
        - form to add new items TODO
        - list of items in the container
    """

    container = Container.query.filter_by(uid=container_id).first()
    items = Item.query.filter_by(container_id=container_id).all()
    space = Space.query.filter_by(uid=container.space_id).first()

    num_tags = len(container.tags())

    form = AddItemForm()

    return render_template(
        'single_container.html',
        container=container,
        items=items,
        form=form,
        space=space,
        make_random_gradient=make_random_gradient,
        num_tags=num_tags,
        search_form=SearchForm()
    )


@container_bp.route('/container/<container_id>/add/item', methods=['POST'])
@login_required
def add_item_to_container(container_id):
    form = AddItemForm()

    # Check the qty input
    if type(form.qty.data) != float:
        flash("Quantity must be a number", "danger")
        return redirect(url_for('container_bp.container_by_id', container_id=container_id))

    # Make the new item
    # -----------------

    item = Item(
        name=form.item_name.data,
        qty=form.qty.data,
        units=form.units.data,
        container_id=container_id
    )

    # tags = Tag.query.filter_by(user_id=current_user.id).all()
    # tag_choices = [t.name for t in tags]
    # form.existing_tags.choices = tag_choices

    # Make a list of all new and existing tags
    all_tags = []
    new_tags = request.form["new_tags"]
    for tag_txt in new_tags.split(","):
        tag_txt = tag_txt.lstrip().rstrip()
        if len(tag_txt) >= 1:
            all_tags.append(tag_txt)

    for tag_txt in form.existing_tags.data:
        all_tags.append(tag_txt)

    # Create each tag if it doesn't exist yet
    tag_list = []

    for tag_txt in all_tags:
        # See if it exists

        tag_txt_as_slug = tag_txt.replace(" ", "-").lower()

        tag = Tag.query.filter_by(
            name=tag_txt_as_slug,
        ).first()
        if tag:
            item.tags.append(tag)
        else:
            tag = Tag(
                name=tag_txt_as_slug,
            )
            db.session.add(tag)
            db.session.commit()

            tag_list.append(tag.uid)

            item.tags.append(tag)

            # flash(f"+ tag {tag.name}", "success")

    db.session.add(item)
    db.session.commit()
    flash(f"+ item {item.name}", "success")


    for error in form.item_name.errors:
        flash(error, "danger")
    for error in form.qty.errors:
        flash(error, "danger")
    for error in form.units.errors:
        flash(error, "danger")
    for error in form.existing_tags.errors:
        flash(error, "danger")
    for error in form.new_tags.errors:
        flash(error, "danger")

    return redirect(url_for('container_bp.container_by_id', container_id=container_id))
