"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    username = StringField(
        'User Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class CategoryForm(FlaskForm):
    """User Log-in Form."""
    category_name = StringField(
        'Category Name',
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField('Add Category')


class ContainerForm(FlaskForm):
    """User Log-in Form."""
    container_name = StringField(
        'Container Name',
        validators=[
            DataRequired(),
        ]
    )
    category = StringField(
        "Category",
        validators=[DataRequired(),]
    )
    submit = SubmitField('Add Container')


def check_length_50(form, field):
    if len(field.data) > 50:
        raise ValidationError('Must be less than 50 characters')
def check_length_25(form, field):
    if len(field.data) > 25:
        raise ValidationError('Must be less than 25 characters')


class SpaceForm(FlaskForm):
    """SPACE"""
    name = StringField(
        'Name',
        validators=[DataRequired(), check_length_25]
    )
    description = StringField(
        'Description',
        validators=[DataRequired(), check_length_50]
    )
    submit = SubmitField('Submit')
