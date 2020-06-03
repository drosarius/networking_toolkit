from flask import Blueprint, render_template, request, session, redirect, \
    url_for
from flask import current_app as app

from application.batfish.batfish import Batfish
from application.batfish.batfish_forms import InitialBatfishForm, BatfishForm

# Set up a Blueprint
batfish_bp = Blueprint('batfish_bp', __name__,
                     template_folder='templates',
                     static_folder='static')






@batfish_bp.route("/batfish", methods=['GET', 'POST'])
def batfish():
    form = InitialBatfishForm()
    if request.method == 'POST' and form.validate_on_submit():
        form = BatfishForm()
        session['batfish_host'] = request.form['batfish_host']
        session['is_new_network'] = request.form.getlist('is_new_network')
        if '1' in request.form.getlist('is_new_network'):
            session['batfish_set_network'] = request.form[
                'batfish_set_network']
            session['snapshot_dir'] = request.form['snapshot_dir']
            session['snapshot_name'] = request.form['snapshot_name']
            return redirect(url_for('batfish_bp.batfish_select_network'))
        return redirect(url_for('batfish_bp.batfish_select_network'))
    return render_template('batfish.html', form=form)



@batfish_bp.route("/batfish_select_network", methods=['GET', 'POST'])
def batfish_select_network():
    form = BatfishForm()
    batfish_host = session['batfish_host']
    batfish = Batfish(batfish_host)
    session['is_new_snapshot'] = request.form.getlist('is_new_snapshot')
    if '1' in session['is_new_network']:
        batfish_set_network = session['batfish_set_network']
        snapshot_dir = session['snapshot_dir']
        snapshot_name = session['snapshot_name']
        batfish.set_network(batfish_set_network)
        batfish.init_snapshot(snapshot_dir, snapshot_name)
    if '1' in session['is_new_snapshot']:
        session['snapshot_dir'] = request.form['snapshot_dir']
        session['snapshot_name'] = request.form['snapshot_name']
        snapshot_dir = session['snapshot_dir']
        snapshot_name = session['snapshot_name']
        batfish.init_snapshot(snapshot_dir, snapshot_name)
    all_networks = batfish.get_existing_networks()
    if request.method == 'POST':
        selected_network = request.form.get('network')
        batfish.set_network(selected_network)
        return redirect(url_for('batfish_bp.batfish_dashboard'))
    return render_template('batfish_select_network.html', form=form,
                           networks=all_networks)


@batfish_bp.route("/batfish_dashboard", methods=['GET', 'POST'])
def batfish_dashboard():
    form = BatfishForm()
    batfish_host = session['batfish_host']
    batfish = Batfish(batfish_host)
    all_snapshots = batfish.get_existing_snapshots()
    if request.method == 'POST' and request.form.get('snapshot') != 'None':
        question_dict = dict(form.pick_question.choices)
        picked_question = question_dict.get(int(form.pick_question.data))
        selected_snapshot = request.form.get('snapshot')
        batfish.set_snapshot(selected_snapshot)
        table = batfish.get_info(picked_question)
        all_snapshots = batfish.get_existing_snapshots()
        return render_template('batfish_data.html', form=form,
                            table=table, snapshots=all_snapshots)
    return render_template('batfish_data.html', form=form, snapshots=all_snapshots)
