from flask_login import current_user
from datetime import datetime
from pytz import timezone
from random import randrange

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from my_stuff import db, make_random_gradient


tag_helper = db.Table(
    'tag_helper',
    db.Column(
        'tag_id',
        db.Integer,
        db.ForeignKey('item_tags.uid'),
        primary_key=True),
    db.Column(
        'item_id',
        db.Integer,
        db.ForeignKey('items.uid'),
        primary_key=True)
)


space_helper = db.Table(
    'space_helper',
    db.Column(
        'space_id',
        db.Integer,
        db.ForeignKey('spaces.uid'),
        primary_key=True),
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('flasklogin_users.id'),
        primary_key=True)
)

class Tag(db.Model):

    __tablename__ = 'item_tags'

    uid = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(25),
        nullable=False,
        unique=True
    )
    background = db.Column(
        db.Text,
        nullable=False,
        unique=False,
        default=make_random_gradient()
    )

    def slug(self):
        return self.name.replace(" ", "-").lower()


class Item(db.Model):

    __tablename__ = 'items'

    uid = db.Column(
        db.Integer,
        primary_key=True
    )
    qty = db.Column(
        db.Float,
        default=1.0,
        nullable=False,
        unique=False,
    )
    units = db.Column(
        db.String(25),
        nullable=False,
        unique=False,
        default="count"
    )
    name = db.Column(
        db.String(50),
        nullable=False,
        unique=False
    )
    container_id = db.Column(
        db.Integer,
        db.ForeignKey("containers.uid"),
        nullable=False
    )
    tags = db.relationship(
        'Tag',
        secondary=tag_helper,
        lazy='subquery',
        backref=db.backref('pages', lazy=True)
    )

    def fancy_units_with_qty(self):
        qty = self.qty
        units = self.units

        qty_as_text = str(qty)
        qty_parts = qty_as_text.split(".")

        if qty_parts[1] == "0":
            fancy_qty = qty_parts[0]
        else:
            fancy_qty = qty_as_text

        if qty == 1 and units == "count":
            return ""
        elif units == "count":
            return f"- {fancy_qty}"
        else:
            return f"- {fancy_qty} {units}"

    def this_container(self):
        return Container.query.filter_by(
            uid=self.container_id
        ).first()

    def this_space(self):
        return Space.query.filter_by(
            uid=self.this_container().space_id
        ).first()

    def container_name(self):
        return self.this_container().name

    def space_name(self):
        return self.this_space().name



class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'flasklogin_users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    website = db.Column(
        db.String(60),
        index=False,
        unique=False,
        nullable=True
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=datetime.now(timezone("US/Eastern")),
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    background = db.Column(
        db.Text,
        nullable=False,
        unique=False,
        default=make_random_gradient()
    )
    spaces = db.relationship(
        'Space',
        secondary=space_helper,
        lazy='subquery',
        backref=db.backref('spaces', lazy=True)
    )

    def num_spaces(self):
        return len(self.spaces)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def track_login(self):
        """Set the last_login value to now """
        self.last_login = datetime.now(timezone("US/Eastern"))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class ContainerCategory(db.Model):

    __tablename__ = 'container_categories'
    __table_args__ = (
        db.UniqueConstraint('name', 'space_id'),
    )

    uid = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(25),
        nullable=False,
        unique=False
    )
    space_id = db.Column(
        db.Integer,
        db.ForeignKey("spaces.uid"),
        nullable=False
    )


class Container(db.Model):

    __tablename__ = 'containers'
    __table_args__ = (
        db.UniqueConstraint('name', 'space_id'),
    )

    uid = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(25),
        nullable=False,
        unique=False
    )
    background = db.Column(
        db.Text,
        nullable=False,
        unique=False,
        default=make_random_gradient()
    )
    lat = db.Column(
        db.Float,
        nullable=True,
        unique=False,
    )
    lng = db.Column(
        db.Float,
        nullable=True,
        unique=False,
    )


    space_id = db.Column(db.Integer, db.ForeignKey("spaces.uid"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("container_categories.uid"), nullable=False)
    items = db.relationship("Item", backref=__tablename__, lazy=True)

    def tags(self):
        all_tags_in_container = []
        for item in self.items:
            for tag in item.tags:
                if tag not in all_tags_in_container:
                    all_tags_in_container.append(tag)
        return sorted(all_tags_in_container, key=lambda t: t.name.lower())

    def num_items(self):
        return len(self.items)

    def category_txt(self):
        category = ContainerCategory.query.filter_by(
            uid=self.category_id
        ).first()
        return category.name

    def space_name(self):
        return Space.query.filter_by(uid=self.space_id).first().name

class Space(db.Model):

    __tablename__ = 'spaces'
    # __table_args__ = (
    #     db.UniqueConstraint('name', 'user_id'),
    # )

    uid = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(25),
        nullable=False,
        unique=False
    )
    description = db.Column(
        db.String(50),
        unique=False,
        nullable=False
    )

    lat = db.Column(
        db.Float,
        nullable=True,
        unique=False,
    )
    lng = db.Column(
        db.Float,
        nullable=True,
        unique=False,
    )

    users = db.relationship(
        'User',
        secondary=space_helper,
        lazy='subquery',
        backref=db.backref('flasklogin_users', lazy=True)
    )

    containers = db.relationship("Container", backref=__tablename__, lazy=True)

    container_categories = db.relationship(
        "ContainerCategory",
        backref=__tablename__,
        lazy=True
    )
    background = db.Column(
        db.Text,
        nullable=False,
        unique=False,
        default=make_random_gradient()
    )

    def num_users(self):
        return len(self.users)

    def share_txt(self):
        if self.num_users() == 1:
            return "Private - not shared with others"
        else:
            other_users = [user.email for user in self.users if user != current_user]
            return "Shared with: " + ", ".join(other_users)