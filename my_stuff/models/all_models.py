from datetime import datetime
from pytz import timezone
from random import randrange

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from my_stuff import db


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


class Tag(db.Model):

    __tablename__ = 'item_tags'
    __table_args__ = (
        db.UniqueConstraint('name', 'user_id'),
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
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("flasklogin_users.id"),
        nullable=False
    )


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


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'flasklogin_users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
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

    spaces = db.relationship("Space", backref=__tablename__, lazy=True)
    tags = db.relationship("Tag", backref=__tablename__, lazy=True)

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

    def __init__(self):
        self.track_login()


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
    space_id = db.Column(db.Integer, db.ForeignKey("spaces.uid"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("container_categories.uid"), nullable=False)



class Space(db.Model):

    __tablename__ = 'spaces'
    __table_args__ = (
        db.UniqueConstraint('name', 'user_id'),
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
    description = db.Column(
        db.String(50),
        unique=False,
        nullable=False
    )
    share_status = db.Column(
        db.String(10),
        unique=False,
        nullable=False,
        default="private"
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("flasklogin_users.id"),
        nullable=False
    )

    container_categories = db.relationship(
        "ContainerCategory",
        backref=__tablename__,
        lazy=True
    )

    def card_background(self, style: str = "random") -> str:

        def _make_random_rgba():
            v1 = randrange(255)
            v2 = randrange(255)
            v3 = randrange(255)

            return f"rgba({v1},{v2},{v3},X)"

        def _gradient(color: str) -> str:
            color1 = color.replace("X", "0.8")
            color2 = color.replace("X", "0")
            return f"{color1}, {color2}"

        # TODO: have style reflect shared vs. private status
        if self.share_status == "private":
            pass
        elif self.share_status == "shared":
            pass

        # For now, just use random colors
        if style == "default":
            color1 = "rgba(255,0,0,X)"
            color2 = "rgba(0,255,0,X)"
            color3 = "rgba(0,0,255,X)"

        elif style == "random":
            color1 = _make_random_rgba()
            color2 = _make_random_rgba()
            color3 = _make_random_rgba()

        rot1 = randrange(360)
        rot2 = randrange(360)
        rot3 = randrange(360)

        text = f"""
            background: linear-gradient({rot1}deg, {_gradient(color1)} 70.71%),
                        linear-gradient({rot2}deg, {_gradient(color2)} 70.71%),
                        linear-gradient({rot3}deg, {_gradient(color3)} 70.71%);
        """

        return text
