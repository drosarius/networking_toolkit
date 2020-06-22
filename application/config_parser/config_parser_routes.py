import os
import uuid

from flask import Blueprint, render_template, request, session, redirect, \
    url_for, json
from flask import current_app as app

# Set up a Blueprint
from flask_wtf import csrf

from application.config_parser import Config_Parser
from application.config_parser.config_parser_forms import ConfigParserForm

config_parser_bp = Blueprint('config_parser_bp', __name__,
                             template_folder='./templates',
                             static_url_path='',
                             static_folder='./static')


@config_parser_bp.route("/config_parser", methods=['GET', 'POST'])
def config_parser():
    form = ConfigParserForm()
    if request.method == 'POST':
        upload_path = "application/config_parser/uploads/" + \
                      str(session["uuid"])
        try:
            os.makedirs(upload_path)
        except OSError:
            print("Failed to create User directory %s" % upload_path)

        input_file = request.files.get(form.inputfile.name)
        input_file.save(upload_path + "/" + input_file.filename)

        if request.get_data():
            data = json.loads(request.get_data())
            device = data['device']
            cli_command = data['command']
            cli_command_dict = dict(form.cli_command.choices)
            command = cli_command_dict.get(int(cli_command))
            table = Config_Parser.config_parse_to_html_table(device,
                                                             command,
                                                             upload_path)
            return table
        cli_command_dict = dict(form.cli_command.choices)
        cli_command = cli_command_dict.get(int(form.cli_command.data))
        table = Config_Parser.config_parse_to_html_table(input_file.filename,
                                                         cli_command,
                                                         upload_path)
        return render_template('config_parser.html', form=form, table=table)

    return render_template('config_parser.html', form=form)