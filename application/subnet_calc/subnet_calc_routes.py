import json
from flask import Blueprint, render_template, request, Response
from application.subnet_calc.subnet_calc_logic import SubnetCalculator
from flask import current_app as app
subnet_calc_bp = Blueprint('subnet_calc_bp', __name__,
                     template_folder='templates',
                     static_folder='static')



@subnet_calc_bp.route("/subnet_calculator", methods=['GET', 'POST'])
def subnet_calculator():
    return render_template('subnet_calculator.html')


@subnet_calc_bp.route("/create_subnet_table", methods=['GET', 'POST'])
def create_subnet_table():
    data = json.loads(request.get_data())
    get_starting_subnet = data['starting_subnet']
    get_split_value = data['split_value']
    subnetcalculator = SubnetCalculator()
    subnets = subnetcalculator.get_subnets(get_starting_subnet,
                                           get_split_value)
    subnet_details = subnetcalculator.get_subnet_details(subnets)
    return Response(json.dumps(subnet_details))



@subnet_calc_bp.route("/split_subnet", methods=['GET', 'POST'])
def split_subnet():
    data = json.loads(request.get_data())
    subnetcalculator = SubnetCalculator()
    subnet_to_be_split = data['subnet_to_be_split']
    subnets = subnetcalculator.get_split_subnets(subnet_to_be_split)
    split_subnet_details = subnetcalculator.get_subnet_details(subnets)
    return Response(json.dumps(split_subnet_details))
