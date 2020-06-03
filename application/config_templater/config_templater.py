from jinja2 import Template, Environment, meta
import pandas as pd
from zipfile import ZipFile
import os

def config_template(config):
    with open('application/config_templater/static/uploads/saved_config_templates/test_template.txt', 'w') as f:
        f.write(config)
    env = Environment()
    test = env.parse(config)
    template_variables = list(meta.find_undeclared_variables(test))
    template_df = pd.DataFrame(columns=template_variables)
    return template_df.to_html(
        classes=["table", "table-bordered", "table-striped", "table-hover"],
        table_id='template_variables_table', header="true")

def get_potential_filenames(config):
    with open('application/config_templater/static/uploads/saved_config_templates/test_template.txt', 'w') as f:
        f.write(config)
    env = Environment()
    test = env.parse(config)
    template_variables = list(meta.find_undeclared_variables(test))
    template_variables.append('index')
    return template_variables



def display_csv(csv_input_file):
    var_csv_df = pd.read_csv("application/config_templater/static/uploads/" + csv_input_file)
    return var_csv_df.to_html(
        classes=["table", "table-bordered", "table-striped", "table-hover"],
        table_id='template_variables_table', header="true")


def config_creator(csv_input_file, filename):
    for subdir, dirs, files in os.walk(
            'application/config_templater/static/Zipped_Config_Templates/'):
        for file in files:
            filePath = os.path.join(subdir, file)
            os.unlink(filePath)
    var_csv_df = pd.read_csv("application/config_templater/static/uploads/" + csv_input_file)
    with open('application/config_templater/static/uploads/saved_config_templates/test_template.txt', 'r') as f:
        config_temp = f.read()
    t = Template(config_temp)
    for index, row in var_csv_df.iterrows():
        config = t.render(**row)
        if filename == 'index':
            with open(
                    'application/config_templater/config_template_storage/' + str(index) + '.txt',
                    'w') as f:
                f.write(config)
        else:
            with open('application/config_templater/config_template_storage/'+ row[filename]  + '.txt', 'w') as f:
                    f.write(config)
    with ZipFile('application/config_templater/static/Zipped_Config_Templates/config_templates.zip', 'w') as zipObj:
        for subdir, dirs, files in os.walk('application/config_templater/config_template_storage/'):
            for file in files:
                filePath = os.path.join(subdir, file)
                zipObj.write(filePath)

    return var_csv_df.to_html(
        classes=["table", "table-bordered", "table-striped", "table-hover"],
        table_id='template_variables_table', header="true")




