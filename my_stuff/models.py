"""Database models."""
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    spaces = db.relationship("Space", backref=__tablename__, lazy=True)

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

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Space(db.Model):

    __tablename__ = 'spaces'

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
    user_id = db.Column(db.Integer, db.ForeignKey("flasklogin_users.id"), nullable=False)

    container_categories = db.relationship("ContainerCategory", backref=__tablename__, lazy=True)
    
    def card_color(self):
        if self.share_status == "private":
            return "#de8cff"
        elif self.share_status == "shared":
            return "#6c138f"


class ContainerCategory(db.Model):

    __tablename__ = 'container_categories'

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


class Container(db.Model):

    __tablename__ = 'containers'

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
