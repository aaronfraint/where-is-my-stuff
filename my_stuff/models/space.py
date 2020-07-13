from random import randrange

from my_stuff import db


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
