
from flask_assets import Environment, Bundle
from flask import current_app as app

def compile_assets(app):
    """Configure authorization asset bundles."""
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False
    config_templater_css_bundle = Bundle('config_templater_bp/styles/config_templater.css',
                              output='dist/css/config_templater.css',
                              extra={'rel': 'stylesheet/css'})
    config_parser_css_bundle = Bundle('config_parser_bp/styles/config_parser.css',
                              output='dist/css/config_parser.css',
                              extra={'rel': 'stylesheet/css'})
    mac_ip_css_bundle = Bundle('mac_ip_bp/styles/mac_ip.css',
                              output='dist/css/mac_ip.css',
                              extra={'rel': 'stylesheet/css'})
    subnet_calc_css_bundle = Bundle('subnet_calc_bp/styles/subnet_calc.css',
                              output='dist/css/subnet_calc.css',
                              extra={'rel': 'stylesheet/css'})

    assets.register('config_templater_css_bundle', config_templater_css_bundle)
    config_templater_css_bundle.build()

    assets.register('config_parser_css_bundle', config_parser_css_bundle)
    config_parser_css_bundle.build()

    assets.register('mac_ip_css_bundle', mac_ip_css_bundle)
    mac_ip_css_bundle.build()

    assets.register('subnet_calc_css_bundle', subnet_calc_css_bundle)
    subnet_calc_css_bundle.build()

