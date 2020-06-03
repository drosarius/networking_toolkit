from flask import request, render_template, Blueprint
from werkzeug.utils import secure_filename

from application.mac_ip.mac_ip import mac_ip_to_html_table
from application.mac_ip.mac_ip_forms import MacIpForm

mac_ip_bp = Blueprint('mac_ip_bp', __name__,
                     template_folder='templates',
                     static_folder='static')



@mac_ip_bp.route("/mac_ip", methods=['GET', 'POST'])
def mac_ip():
    form = MacIpForm()
    if request.method == 'POST':
        mac_input_file = secure_filename(form.mac_inputfile.data.filename)
        form.mac_inputfile.data.save('application/mac_ip/uploads/' + mac_input_file)
        arp_input_file = secure_filename(form.arp_inputfile.data.filename)
        form.arp_inputfile.data.save('application/mac_ip/uploads/' + arp_input_file)
        table = mac_ip_to_html_table(mac_input_file, arp_input_file)
        return render_template('mac_ip.html', form=form, table=table)
    return render_template('mac_ip.html', form=form)
