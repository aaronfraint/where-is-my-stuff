
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextField, SelectMultipleField
from wtforms.validators import DataRequired, Length


class AddItemForm(FlaskForm):
    """
    Form on page for a single container.

    """

    item_name = StringField(
        "Item Name",
    )
    qty = FloatField(
        "Quantity",
    )
    units = StringField(
        "Item Name",
    )
    existing_tags = SelectMultipleField(
        "Existing Tags",
    )
    new_tags = TextField(
        "New Tags",
    )

    submit = SubmitField('Add Item')
