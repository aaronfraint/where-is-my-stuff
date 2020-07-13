"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AddSpaceForm(FlaskForm):
    """
    Form on page for all spaces.

    Allows user to add a new space.
    """

    space_name = StringField(
        "Name",
        validators=[
            DataRequired(message="Please provide a name for your new space"),
            Length(min=1, max=25, message="Space name must be less than 25 characters."),
        ]
    )
    description = StringField(
        "Description",
        validators=[
            DataRequired(message="Please add a description for your space."),
            Length(min=1, max=50, message="Description must be less than 50 characters."),
        ]
    )
    submit = SubmitField('Add Space')
