from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, FileField, BooleanField, \
    MultipleFileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, IPAddress
import os




class ConfigTemplaterForm(FlaskForm):
    variable_csv = FileField(u'Choose CSV')
    ready = SubmitField('Ready')
    set = SubmitField('Set')