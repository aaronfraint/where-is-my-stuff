from my_stuff import db


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
