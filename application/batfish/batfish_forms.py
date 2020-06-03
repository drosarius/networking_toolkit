from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, FileField, BooleanField, \
    MultipleFileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, IPAddress
import os



class InitialBatfishForm(FlaskForm):
    batfish_host = StringField('batfish Host',
                           validators=[DataRequired(), IPAddress()])
    snapshot_name = StringField('Snapshot Name')
    set_snapshot = StringField('Set Snapshot')
    batfish_set_network = StringField('Set Network')
    snapshot_dir = StringField('Snapshot Directory')
    submit = SubmitField('Go!')

class BatfishForm(FlaskForm):
    batfish_question_list = ["ipOwners",
                            "nodeProperties",
                            "routes",
                            "layer3Edges",
                            "interfaceProperties",
                            "namedStructures",
                            "definedStructures",
                            "referencedStructures",
                            "unusedStructures",
                            "undefinedReferences",
                            "switchedVlanProperties",
                            "bgpProcessConfiguration",
                            "bgpPeerConfiguration",
                            "bgpSessionCompatibility",
                            "bgpSessionStatus",
                            "bgpEdges",
                            "ospfInterfaceConfiguration",
                            "ospfProcessConfiguration",
                            "ospfSessionCompatibility",
                            "ospfEdges",
                            "ospfAreaConfiguration",
                            "loopbackMultipathConsistency",
                            "filterLineReachability",
                            "initIssues",
                            "fileParseStatus",
                            "parseWarning",
                            "vxlanVniProperties",
                            "vxlanEdges",
                            "evpnL3VniProperties",
                            "detectLoops"]
    pick_question_list = [(i, j) for i, j in zip(list(range(len(batfish_question_list))), batfish_question_list)]
    batfish_set_network = StringField('Set Network')
    batfish_host = StringField('batfish Host',
                           validators=[DataRequired(), IPAddress()])
    snapshot_dir = StringField('Snapshot Directory')
    overwrite = BooleanField("Overwrite?")
    snapshot_name = StringField('Snapshot Name')
    set_snapshot = StringField('Set Snapshot')
    pick_question = SelectField(u'Pick a Question',
                              choices=pick_question_list)
    submit = SubmitField('Go!')
    reset = SubmitField('Reset')

    export = SubmitField('Export')