from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, FileField, BooleanField, \
    MultipleFileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, IPAddress
import os






class MacIpForm(FlaskForm):
    mac_inputfile = FileField(validators=[DataRequired()])
    arp_inputfile = FileField(validators=[DataRequired()])
    submit = SubmitField('Go!')
