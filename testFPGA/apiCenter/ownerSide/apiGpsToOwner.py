from crypt import methods
from flask import Blueprint, jsonify, request
from flask_login import login_required
from ..model import vehicleDetails
from sqlalchemy import text,select
from .. import db
ownerGPSauth = Blueprint("ownerGPSauth",__name__)



######################    current gps location      ####################################

@ownerGPSauth.route("/api/gpsLocationCurrent/",methods=['POST'])

def gpsLocationCurrent():
    code_ = str(request.json.get('vehicleCode'))

    result=db.session.execute(text("SELECT * FROM vehicle_details WHERE vehicleCode_ == '"+code_+"'"))
    result = result.mappings().all()
    
    try:
        return jsonify({"gpsLocation":str(result[-1]['gpsPointCurr_'])}),201   #last gps point that vehicle left
    except:
        return "No Data found",200


######################    last gps track of vehicle covered      ########################

@ownerGPSauth.route("/api/gpsLocationTrack/",methods=['POST'])
@login_required
def gpsLocationTrack():
    code_ = str(request.json.get('vehicleCode'))
    _conn =db.session.execute(text("SELECT * FROM vehicle_details WHERE status_ == 'inActive' AND vehicleCode_ == '"+code_+"'"))
    _conn = _conn.mappings().all()
    id_ = str(_conn[-1]['id'])
    result =db.session.execute(text("SELECT * FROM vehicle_details WHERE vehicleCode_ == '"+code_+"' AND id >= "+id_))
    result_ = result.mappings().all()
    #id_ = _conn[-1]['id']
    track=[]
    for i in result_:
        track.append(i['gpsPointCurr_'])

    return jsonify(track),201     #track of gps point from last inActive of vehicle



############ list of gps locations coverd by vehcile in multiple instance   ##############

@ownerGPSauth.route("/api/gpsLocationCovered/" , methods=['POST'])
@login_required
def gpsLocationCovered():
    code_ = str(request.json.get('vehicleCode'))
    _conn =db.session.execute(text("SELECT * FROM vehicle_details WHERE status_ == 'inActive' AND vehicleCode_ == '"+code_+"'"))
    _conn = _conn.mappings().all()
    instances_ = []
    for i in _conn:
        instances_.append(i['id'])
    
    instantTrack_ ={}
    count_=1
    for iter in range(len(instances_)-1):
        query_= "SELECT * FROM vehicle_details WHERE vehicleCode_ == '"+code_+"' AND id BETWEEN "+str(instances_[iter])+" AND "+str(instances_[iter]+1)
        _track =db.session.execute(text(query_))
        result_ = _track.mappings().all()
        track=[]
        for i in result_:
            track.append(i['gpsPointCurr_'])
        instantTrack_[count_]=track
        count_+=1
    
    return jsonify(instantTrack_),201



