import textfsm
import pandas as pd



def config_parse_to_html_table(input_file, command):
    input_file = open("application/config_parser/uploads/" + input_file, encoding='utf-8')
    cli_data = input_file.read()
    input_file.close()


    with open("application/static/ntc_templates/" + command) as f:
        template = textfsm.TextFSM(f)
    fsm_results = template.ParseText(cli_data)
    df = pd.DataFrame(columns=template.header, data=fsm_results)
    return df.to_html(classes=["table", "table-bordered", "table-striped", "table-hover"], table_id='parsed_config_table', index=False, border=0)
