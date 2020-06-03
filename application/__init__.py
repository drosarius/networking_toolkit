
"""Initialize app."""
from flask import Flask
from flask_wtf import csrf
from flask_wtf.csrf import CSRFProtect, CsrfProtect

from config import Config
from .batfish import batfish_routes
from .config_parser import config_parser_routes
from .config_templater import config_templater_routes
from .mac_ip import mac_ip_routes
from .subnet_calc import subnet_calc_routes
from .mop_creator import mop_creator_routes


def create_app(config_class=Config):
    """Construct the core application."""
    app = Flask(__name__,
                instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config['SECRET_KEY'] = '664b4b9ece7a544d8fa77d15704512ef'
    app.config["CONFIG_TEMPLATES"] = "application/config_templater/zipped_config_storage"
    csrf = CsrfProtect(app)

    with app.app_context():

        # Import main Blueprint
        from application import routes
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(batfish_routes.batfish_bp)
        app.register_blueprint(config_parser_routes.config_parser_bp)
        app.register_blueprint(config_templater_routes.config_templater_bp)
        app.register_blueprint(mac_ip_routes.mac_ip_bp)
        app.register_blueprint(subnet_calc_routes.subnet_calc_bp)
        app.register_blueprint(mop_creator_routes.mop_creator_bp)
        # app.register_blueprint(batfish_dash_routes.batfish_dash_bp)
        #
        # csrf.exempt(batfish_dash_routes.batfish_dash_bp)
        csrf.exempt(config_parser_routes.config_parser_bp)
        csrf.exempt(mop_creator_routes.mop_creator_bp)
        csrf.exempt(subnet_calc_routes.subnet_calc_bp)
        csrf.exempt(mac_ip_routes.mac_ip_bp)
        csrf.exempt(config_templater_routes.config_templater_bp)
        csrf.exempt(batfish_routes.batfish_bp)
        # csrf.exempt('dash.dash.dispatch')
        # Import Dash application


        # Compile assets
        from application.assets import compile_assets
        compile_assets(app)

        return app