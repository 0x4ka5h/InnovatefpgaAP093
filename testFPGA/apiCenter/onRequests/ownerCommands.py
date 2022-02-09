from sqlalchemy import text
from flask_login import login_required
from flask import Blueprint, jsonify, redirect, request, url_for
from ..model import ownerCommands,remoteControlValues,valuesForRemoteAccess
from .. import db

ownerCommandsauth = Blueprint("ownerCommandsauth",__name__)


@ownerCommandsauth.route("/api/commands/commandsPassing/",methods=['POST'])
@login_required

def commandsPassing():
    
    modeChange_ = str(request.json.get('mode')) 
    cameraView_ = str(request.json.get('view'))
      # 0-Normal , 1-Remote mode , 2-AutoMode
      # 0-off , 1-inside camera view , 2-outsideView

    #if db.session.query(ownerCommands).filter_by(_timeStamp=_timeStamp).count() < 1:
    commands_ = ownerCommands(modeChange_= modeChange_,cameraView_ = cameraView_)
    db.session.add(commands_)
    db.session.commit()
    if modeChange_ == '1':
      rcToVehicle = remoteControlValues(steerAngle_= 0,\
                            breakFunc_=0,\
                            acccelarationFunc_=0)
      db.session.add(rcToVehicle)
      db.session.commit()
      rcParameters = valuesForRemoteAccess(speed_= 0,\
                            ultraSonicLeft_=0,\
                            ultraSonicRight_ = 0,\
                            ultraSonicBack1_ = 0 )
      db.session.add(rcParameters)
      db.session.commit()
    if modeChange_ == '0' or modeChange_=='2':
      
      delete_q = remoteControlValues.__table__.delete().where(remoteControlValues.steerAngle_ == 0, \
                            remoteControlValues.breakFunc_==0,\
                            remoteControlValues.acccelarationFunc_==0)
      db.session.execute(delete_q)
      db.session.commit()

      delete_q = valuesForRemoteAccess.__table__.delete().where(valuesForRemoteAccess.speed_ == 0, \
                            valuesForRemoteAccess.ultraSonicLeft_==0,\
                            valuesForRemoteAccess.ultraSonicRight_==0,\
                            valuesForRemoteAccess.ultraSonicBack1_==0)
      db.session.execute(delete_q)
      db.session.commit()

    
    return jsonify({'request': "Success"}), 201



@ownerCommandsauth.route("/api/commands/retrieveOwnerCommands/",methods=['GET'])
@login_required

def retrieveOwnerCommands():
    query = "SELECT * FROM owner_commands"
    result_= db.session.execute(text(query))
    _conn = result_.mappings().all()
    mode = _conn[-1]['modeChange_']
    view = _conn[-1]['cameraView_']
    print({"mode":mode,"view":view})

    return jsonify({"mode":mode,"view":view}),201
