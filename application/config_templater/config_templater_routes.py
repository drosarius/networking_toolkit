import os
import time

from flask import current_app as app, send_file, url_for
from flask import request, session, render_template, after_this_request, app, \
    Blueprint, send_from_directory, abort
from werkzeug.utils import secure_filename
from application.config_templater.config_templater import config_template, \
    get_potential_filenames, display_csv, config_creator, delete_old_files
from application.config_templater.config_templater_forms import \
    ConfigTemplaterForm
# Set up a Blueprint
from flask_wtf import csrf


config_templater_bp = Blueprint('config_templater_bp', __name__,
                                template_folder='templates',
                                static_url_path='',
                                static_folder='./static')


@config_templater_bp.route("/config_templater", methods=['GET', 'POST'])
def config_templater():
    form = ConfigTemplaterForm()
    config = ''
    potential_filenames = []
    if request.method == 'POST':
        config = request.form['my-xml-editor']
        table = config_template(config)
        potential_filenames = get_potential_filenames(config)
        if form.variable_csv.data.filename != '':
            csv_input_file = secure_filename(form.variable_csv.data.filename)
            session['csv_input_file'] = secure_filename(form.variable_csv.data.filename)

            form.variable_csv.data.save('application/config_templater/uploads/' + csv_input_file)
            table = display_csv(csv_input_file)
            potential_filenames = get_potential_filenames(config)
            return render_template('config_templater.html', form=form, potential_filenames=potential_filenames,
                                   table=table, config=config)
        return render_template('config_templater.html', form=form, table=table,  potential_filenames=potential_filenames, config=config)
    return render_template('config_templater.html', form=form,  potential_filenames=potential_filenames, config=config)



@config_templater_bp.route("/get_config_templates/<filename>", methods=['GET', 'POST'])
def get_config_templates(filename):
    config_creator(session['csv_input_file'], filename)
    @after_this_request
    def remove_files(response):
        try:
            info_to_delete = ['application/config_templater/config_template_storage',
                              'application/config_templater/uploads/saved_config_templates',
                              'application/config_templater/uploads']
            delete_old_files(info_to_delete)

        except Exception as error:
            app.logger.error(
                "Error removing or closing downloaded file handle", error)
        return response

    try:
        return config_templater_bp.send_static_file('Zipped_Config_Templates/config_templates.zip')

    except FileNotFoundError:
        abort(404)
