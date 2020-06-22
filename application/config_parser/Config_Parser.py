import textfsm
import pandas as pd
import os
import shutil




def config_parse_to_html_table(input_file, command, upload_path):
    with open(upload_path + "/" + input_file, encoding='utf-8') as f:
        cli_data = f.read()
    try:
        shutil.rmtree(upload_path)
    except Exception:
        print("Failed to delete directory %s" % upload_path)

    with open("application/static/ntc_templates/" + command) as f:
        template = textfsm.TextFSM(f)
    fsm_results = template.ParseText(cli_data)
    df = pd.DataFrame(columns=template.header, data=fsm_results)
    return df.to_html(classes=["table", "table-bordered", "table-striped", "table-hover"], table_id='parsed_config_table', index=False, border=0)
