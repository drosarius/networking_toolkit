from flask import Flask, render_template, Blueprint
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from flask import current_app as app
import dash
import dash_core_components as dcc
import dash_html_components as html



main_bp = Blueprint('main_bp', __name__,
                     template_folder='templates',
                     static_folder='static')


@main_bp.route("/")
@main_bp.route("/home")
def home():
    date_time = datetime.now()
    return render_template('home.html', date_time=date_time
                           .strftime("%m/%d/%Y, %H:%M"))







