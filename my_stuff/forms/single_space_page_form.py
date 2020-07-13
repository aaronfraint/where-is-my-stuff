"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, NoneOf


class AddContainerForm(FlaskForm):
    """
    Form on page for a single space.

    Allows user to add a new container
    and either use an existing category
    or add a new category.
    """

    container_name = StringField(
        "Container Name",
        validators=[
            DataRequired(message="Please provide a name for your new container"),
            Length(min=1, max=25),
        ]
    )
    new_category = StringField(
        "New Category",
        validators=[
        ]
    )
    existing_category = StringField(
        "Existing Category",
        validators=[]
    )
    submit = SubmitField('Add Category')
