from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FileField
from wtforms.validators import DataRequired
import os





class ConfigParserForm(FlaskForm):
    list_of_templates = os.listdir('application/static/ntc_templates')
    num_of_templates = len(list_of_templates)
    cli_command_list = [(i, j) for i, j in zip(list(range(num_of_templates)), list_of_templates)]
    inputfile = FileField(validators=[DataRequired()])
    cli_command = SelectField(u'Pick a command',
                              choices=cli_command_list)
    submit = SubmitField('Go!')