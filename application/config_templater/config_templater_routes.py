import io
import os
import pathlib
import zipfile
from flask import current_app as app, send_file
from flask import request, session, render_template, after_this_request, app, \
    Blueprint, abort
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
    upload_path = "application/config_templater/uploads/" + \
                  str(session["uuid"])
    try:
        os.makedirs(upload_path)
    except OSError:
        print("Failed to create User directory %s" % upload_path)

    if request.method == 'POST':
        config = request.form['my-xml-editor']
        table = config_template(config, upload_path)
        potential_filenames = get_potential_filenames(config, upload_path)
        if form.variable_csv.data.filename != '':
            csv_input_file = secure_filename(form.variable_csv.data.filename)
            session['csv_input_file'] = secure_filename(form.variable_csv.data.filename)
            form.variable_csv.data.save(upload_path + "/" + csv_input_file)
            table = display_csv(csv_input_file, upload_path)
            potential_filenames = get_potential_filenames(config, upload_path)
            return render_template('config_templater.html', form=form, potential_filenames=potential_filenames,
                                   table=table, config=config)
        return render_template('config_templater.html', form=form, table=table,  potential_filenames=potential_filenames, config=config)
    return render_template('config_templater.html', form=form,  potential_filenames=potential_filenames, config=config)



@config_templater_bp.route("/get_config_templates/<filename>", methods=['GET', 'POST'])
def get_config_templates(filename):
    upload_path = "application/config_templater/uploads/" + \
                  str(session["uuid"])
    config_creator(session['csv_input_file'],
                   filename,
                   upload_path,
                   str(session["uuid"]))
    @after_this_request
    def remove_files(response):
        try:
            delete_old_files(upload_path)

        except Exception as error:
            app.logger.error(
                "Error removing or closing downloaded file handle", error)
        return response

    created_template_path = upload_path + "/created_templates"
    base_path = pathlib.Path(created_template_path)
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)

    try:
        return send_file(data,
                         mimetype='application/zip',
                         as_attachment=True,
                         attachment_filename='config_template.zip'
                         )

    except FileNotFoundError:
        abort(404)





