import json
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



@ownerCommandsauth.route("/api/commands/retrieveOwnerCommands/")
#@login_required

def retrieveOwnerCommands():
    query = "SELECT * FROM owner_commands"
    result_= db.session.execute(text(query))
    _conn = result_.mappings().all()
    mode = _conn[-1]['modeChange_']
    view = _conn[-1]['cameraView_']
    print({"mode":mode,"view":view})

    return jsonify({"mode":mode,"view":view}),201

@ownerCommandsauth.route("/api/sendRFSDetails/",methods=['POST'])
#@login_required

def sendRFSDetails():
    data = request.json
    
#    data = request.json.get('rfsData')
    f = open('apiCenter/ownerSide/RFSdata.txt','w+')
    json_object = json.dumps(data, indent = 4)
    f.write(json_object)
    f.close()
    return "Ok",200



@ownerCommandsauth.route("/api/requestRFSDetails/")
@login_required

def requestRFSDetails():
    f = open('apiCenter/ownerSide/RFSdata.txt','r+')
    data = json.load(f)
    f.close()
    #data = json.dump(data)
    data = jsonify(data)
    #print(type(data))
    
    data.headers.add("Access-Control-Allow-Origin", "*")
    return data


@ownerCommandsauth.route("/api/sendautoInstruction/",methods=['POST'])
@login_required
def sendautoInstruction():
    data = request.json
    if data['gps']=='0' and data['pPath']==1:
        _conn =db.session.execute(text("SELECT * FROM vehicle_details WHERE status_ == 'inActive' AND vehicleCode_ == 'ap093'"))
        _conn = _conn.mappings().all()
        id_ = str(_conn[-1]['id'])
        result =db.session.execute(text("SELECT * FROM vehicle_details WHERE vehicleCode_ == 'ap093' AND id >= "+id_))
        result_ = result.mappings().all()
        #id_ = _conn[-1]['id']
        track=[]
        for i in result_:
            track.append(i['gpsPointCurr_'])
        data['location'] = str(track[0])
    else:
        data['location'] = 0
#    data = request.json.get('rfsData')
    f = open('apiCenter/ownerSide/path.txt','w+')
    json_object = json.dumps(data, indent = 4)
    f.write(json_object)
    f.close()
    return "Ok",200



@ownerCommandsauth.route("/api/requestautoInstruction/")
@login_required
def requestautoInstruction():
    f = open('apiCenter/ownerSide/path.txt','r+')
    data = json.load(f)
    f.close()
    #data = json.dump(data)
    data = jsonify(data)
    #print(type(data))
    
    data.headers.add("Access-Control-Allow-Origin", "*")
    return data
