from flask import Blueprint, render_template, request, session, redirect, \
    url_for, json
from flask import current_app as app

# Set up a Blueprint
from flask_wtf import csrf

from application.config_parser import Config_Parser
from application.config_parser.config_parser_forms import ConfigParserForm

config_parser_bp = Blueprint('config_parser_bp', __name__,
                     template_folder='templates',
                     static_folder='static')





@config_parser_bp.route("/config_parser", methods=['GET', 'POST'])
def config_parser():
    form = ConfigParserForm()
    devices = []
    if request.method == 'POST':
        input_files = request.files.getlist(form.inputfile.name)
        for files in input_files:
            files.save('application/config_parser/uploads/' + files.filename)
            devices.append(files.filename)
        if request.get_data():
            data = json.loads(request.get_data())
            device = data['device']
            cli_command = data['command']
            cli_command_dict = dict(form.cli_command.choices)
            command = cli_command_dict.get(int(cli_command))
            table = Config_Parser.config_parse_to_html_table(device,
                                                             command)
            return table
        cli_command_dict = dict(form.cli_command.choices)
        cli_command = cli_command_dict.get(int(form.cli_command.data))
        table = Config_Parser.config_parse_to_html_table(devices[0], cli_command)
        return render_template('config_parser.html', form=form, table=table, devices=devices)

    return render_template('config_parser.html', form=form, devices=devices)