import shutil
from jinja2 import Template, Environment, meta
import pandas as pd
from zipfile import ZipFile
import os

def delete_old_files(upload_path):
    try:
        shutil.rmtree(upload_path)
    except Exception:
        print("Failed to delete directory %s" % upload_path)


def get_template_variables(config, upload_path):
    with open(upload_path + "/test_template.txt", 'w') as f:
        f.write(config)
    env = Environment()
    parsed_config = env.parse(config)
    result = list(meta.find_undeclared_variables(parsed_config))
    return result


def config_template(config, upload_path):
    template_vars = get_template_variables(config, upload_path)
    template_df = pd.DataFrame(columns=template_vars)
    return template_df.to_html(
        classes=["table", "table-bordered", "table-striped", "table-hover"],
        table_id='template_variables_table', header="true")

def get_potential_filenames(config, upload_path):
    template_vars = get_template_variables(config, upload_path)
    template_vars.append('index')
    return template_vars


def display_csv(csv_input_file, upload_path):
    var_csv_df = pd.read_csv(upload_path + "/" + csv_input_file)
    return var_csv_df.to_html(
        classes=["table", "table-bordered", "table-striped", "table-hover"],
        table_id='template_variables_table', header="true")


def config_creator(csv_input_file, filename, upload_path, uuid):
    try:
        os.makedirs(upload_path + "/created_templates")
    except OSError:
        print("Failed to create User directory %s" % upload_path)

    created_template_dir = upload_path + "/created_templates"
    var_csv_df = pd.read_csv(upload_path + "/" + csv_input_file)
    with open(upload_path + "/test_template.txt", 'r') as f:
        config_temp = f.read()
    t = Template(config_temp)
    for index, row in var_csv_df.iterrows():
        config = t.render(**row)
        if filename == 'index':
            with open(
                    created_template_dir + '/' + str(index) + '.txt',
                    'w') as f:
                f.write(config)
        else:
            with open(created_template_dir + '/' + row[filename]  + '.txt', 'w') as f:
                    f.write(config)





