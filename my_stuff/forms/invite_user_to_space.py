"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class InviteForm(FlaskForm):
    """Invite another user to a space """
    invite_email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired(message="Please provide the email address of the person you want to share with.")
        ]
    )
    submit = SubmitField('Invite')
