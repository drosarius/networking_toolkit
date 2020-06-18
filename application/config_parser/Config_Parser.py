import textfsm
import pandas as pd
import os



def config_parse_to_html_table(input_file, command):
    with open("application/config_parser/uploads/" + input_file, encoding='utf-8') as f:
        cli_data = f.read()
    try:
        for subdir, dirs, files in os.walk(r"application/config_parser/uploads"):
            for file in files:
                filePath = os.path.join(subdir, file)
                os.unlink(filePath)

    except Exception as error:
        print(error)

    with open("application/static/ntc_templates/" + command) as f:
        template = textfsm.TextFSM(f)
    fsm_results = template.ParseText(cli_data)
    df = pd.DataFrame(columns=template.header, data=fsm_results)
    return df.to_html(classes=["table", "table-bordered", "table-striped", "table-hover"], table_id='parsed_config_table', index=False, border=0)
