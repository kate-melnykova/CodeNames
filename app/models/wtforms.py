from typing import List

from wtforms import Form
from wtforms import StringField
from wtforms import Field, PasswordField, BooleanField, DateField, TextAreaField
from wtforms.validators import ValidationError
from wtforms.fields.html5 import EmailField
from wtforms import validators


strip_filter = lambda x: x.strip() if x else None


def no_special_symbols(form, field):
    if not all(char.isalnum() for char in field.data):
        raise ValidationError('Field has characters that are not allowed!')


class CreateGameForm(Form):
    name = StringField('Enter your name*:', [validators.DataRequired(),
                                             validators.Length(min=1, max=15),
                                             no_special_symbols,
                                             ])
    codemaster = BooleanField('I want to be a codemaster (program selects randomly)')
    join = StringField('If you want to join the game, please enter 4-char code')


