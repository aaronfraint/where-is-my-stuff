"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    """Invite another user to a space """
    search_txt = StringField(
        'Search',
    )
    submit = SubmitField('?')
