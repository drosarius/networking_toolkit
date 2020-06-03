import json
import time
from flask import Blueprint, render_template, request, Response
from flask import current_app as app
mop_creator_bp = Blueprint('mop_creator_bp', __name__,
                     template_folder=r'C:\Users\drosarius\Desktop\Network_Toolkit\networking_toolkit\react-flask-app\public',
                     static_folder='static')



@mop_creator_bp.route("/mop_creator", methods=['GET', 'POST'])
def mop_creator():
    return render_template('index.html')