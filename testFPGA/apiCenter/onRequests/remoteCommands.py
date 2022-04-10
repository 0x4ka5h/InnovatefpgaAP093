from sqlalchemy import text
from flask_login import login_required
from flask import Blueprint, jsonify, redirect, request, url_for
from ..model import valuesForRemoteAccess,remoteControlValues
from .. import db

remoteCommandsauth = Blueprint("remoteCommandsauth",__name__)


@remoteCommandsauth.route('/api/fromOwner/forRemote/remoteCommandsToVehicle/',methods=['POST'])
@login_required
def remoteCommandsToVehicle():

    steerAngle_ = request.json.get('steerAngle')
    breakFunc_ = request.json.get('breakFunc')
    acccelarationFunc_ = request.json.get('acccelarationFunc')

    rcToVehicle = remoteControlValues(steerAngle_=steerAngle_,\
                            breakFunc_=breakFunc_,\
                            acccelarationFunc_=acccelarationFunc_)
    db.session.add(rcToVehicle)
    db.session.commit()
    return jsonify({'request': "Success"}), 201


@remoteCommandsauth.route('/api/fromOwner/forRemote/retrieveRemoteCommands/')
#@login_required
def retrieveRemoteCommands():
    query_ = "SELECT * FROM remote_control_values WHERE steerAngle_ = 0 AND breakFunc_ = 0 AND acccelarationFunc_= 0"
    _conn = db.session.execute(text(query_))
    _conn = _conn.mappings().all()
    id_=None
    try:
        query__ = "SELECT * FROM remote_control_values"

        _conn_ = db.session.execute(text(query__))
        
        _conn = _conn_.mappings().all()

        id_ = str(_conn[-1]['id'])
        
    except:
        pass
    print(id_)
    if id_:
        result =db.session.execute(text("SELECT * FROM remote_control_values"))# WHERE id >="+str(id)))
        result_ = result.mappings().all()
        steerAngle_ = result_[-1]['steerAngle_']
        breakFunc_ = result_[-1]['breakFunc_']
        acccelarationFunc_ = result_[-1]['acccelarationFunc_']

        return jsonify({'steerAngle_':steerAngle_,\
                        'breakFunc_':breakFunc_,\
                        'acccelarationFunc_':acccelarationFunc_}),201

    return "No Data Found",200




@remoteCommandsauth.route('/api/fromVehicle/forRemote/parameterForRC/',methods=['POST'])
@login_required
def parameterForRC():

    speed_ = request.json.get('speed')
    ultraSonicLeft_ = request.json.get('usLeft')
    ultraSonicRight_ = request.json.get('usRight')
    ultraSonicBack1_ = request.json.get('usBack')
    rcParameters = valuesForRemoteAccess(speed_=speed_,\
                            ultraSonicLeft_= ultraSonicLeft_,\
                            ultraSonicRight_ = ultraSonicRight_,\
                            ultraSonicBack1_ = ultraSonicBack1_ )
    db.session.add(rcParameters)
    db.session.commit()
    return jsonify({'request': "Success"}), 201


@remoteCommandsauth.route('/api/fromVehicle/forRemote/retrieveforRC/')
@login_required
def retrieveforRC():
    query_ = "SELECT * FROM values_for_remote_access WHERE speed_ = 0 AND ultraSonicLeft_ = 0 AND ultraSonicRight_= 0 AND ultraSonicBack1_= 0"
    _conn = db.session.execute(text(query_))
    _conn = _conn.mappings().all()
    id_=None
    try:
        query__ = "SELECT * FROM values_for_remote_access"
        _conn_ = db.session.execute(text(query__))
        _conn_ = _conn_.mappings().all()
        print(_conn_)
        id_ = str(_conn[-1]['id'])
    except:
        pass
    if id_:
        result =db.session.execute(text("SELECT * FROM values_for_remote_access"))
        result_ = result.mappings().all()
        speed_ = result_[-1]['speed_']
        ultraSonicLeft_ = result_[-1]['ultraSonicLeft_']
        ultraSonicBack1_ = result_[-1]['ultraSonicBack1_']
        ultraSonicRight_ = result_[-1]['ultraSonicRight_']


        return jsonify({'ultraSonicLeft_':ultraSonicLeft_,\
                        'ultraSonicRight_':ultraSonicRight_,\
                        'speed_':speed_,'ultraSonicBack1_':ultraSonicBack1_ }),201

    return "No Data Found",200