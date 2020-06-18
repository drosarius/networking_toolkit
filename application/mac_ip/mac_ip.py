import pandas as pd
import textfsm
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def delete_old_files(path):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            filePath = os.path.join(subdir, file)
            os.unlink(filePath)


def mac_ip_to_html_table(mac_table, arp_table):
    mac_table_template ="application/static/ntc_templates/cisco_ios_show_mac-address-table.textfsm"
    arp_table_template = "application/static/ntc_templates/cisco_ios_show_ip_arp.textfsm"

    mac_input_file = open("application/mac_ip/uploads/" + mac_table, encoding='utf-8')
    mac_cli_data = mac_input_file.read()
    mac_input_file.close()

    arp_input_file = open("application/mac_ip/uploads/" + arp_table, encoding='utf-8')
    arp_cli_data = arp_input_file.read()
    arp_input_file.close()

    with open(mac_table_template) as f:
        mac_template = textfsm.TextFSM(f)
    mac_fsm_results = mac_template.ParseText(mac_cli_data)
    with open(arp_table_template) as f:
        arp_template = textfsm.TextFSM(f)
    arp_fsm_results = arp_template.ParseText(arp_cli_data)
    mac_df = pd.DataFrame(columns=mac_template.header, data=mac_fsm_results)
    arp_df = pd.DataFrame(columns=arp_template.header, data=arp_fsm_results)
    mac_df['NEW_MAC'] = mac_df['DESTINATION_ADDRESS'].str.extract('(^[\w].{6})', expand=True)
    mac_df['NEW_MAC'] = mac_df['NEW_MAC'].str.replace(r'.', '')
    oui = pd.read_csv(
        'application/mac_ip/static/macaddress.io-db.csv')
    oui['oui'] = oui['oui'].str.replace(r':', '').str.lower()
    merged_df = pd.merge(mac_df, arp_df, left_on='DESTINATION_ADDRESS', right_on='MAC')
    new_merge_df = pd.merge(merged_df, oui, left_on='NEW_MAC', right_on='oui')
    final_df = new_merge_df[['DESTINATION_ADDRESS', 'VLAN', 'DESTINATION_PORT', 'ADDRESS', 'companyName']]
    delete_old_files('application/mac_ip/uploads')
    return final_df.to_html(classes=["table", "table-bordered", "table-striped", "table-hover"], table_id='mac_ip_vendor_table', header="true", index=False, border=0)





