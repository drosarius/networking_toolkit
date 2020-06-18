from flask import Flask, render_template, Blueprint
from flask import current_app as app




main_bp = Blueprint('main_bp', __name__,
                     template_folder='templates',
                     static_folder='static')


@main_bp.route("/")
@main_bp.route("/home")
def home():
    return render_template('home.html')







