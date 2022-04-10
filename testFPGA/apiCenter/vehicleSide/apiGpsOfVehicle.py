from flask_login import login_required
from flask import Blueprint, jsonify, redirect, request, url_for
from ..model import vehicleDetails
from .. import db
from flask_login import login_required, current_user

vehicleGPSauth = Blueprint("vehicleGPSauth",__name__)


@vehicleGPSauth.route("/api/vehicle/sendVehicleDetails/" , methods = ['POST'])
@login_required

def sendVehicleDetails():
    
    vehicleCode_ = request.json.get('vehicleCode')
    status_ = request.json.get('status')
    timeStamp_ = request.json.get('timeStamp')
    driver_ = request.json.get('driver')
    mode_ = request.json.get('mode')
    gpsPointCurr_ = request.json.get('gpsPoint')

    if db.session.query(vehicleDetails).filter_by(timeStamp_=timeStamp_).count() < 1:
        details_ = vehicleDetails(vehicleCode_= vehicleCode_,\
            status_ = status_,\
            timeStamp_=timeStamp_,\
            driver_=driver_,\
            mode_= mode_,\
            gpsPointCurr_=gpsPointCurr_)

        db.session.add(details_)
        db.session.commit()   # add the details to the database
    else:
        return jsonify({ 'request': "failed" ,"Reason" : "timeStamp should be Unique"}), 201
    
    return jsonify({'request': "Success"}), 201




'''
@vehicleGPSauth.route("/api/vehicle/details/")
@login_required
def fetchDetails():
    userId = current_user.username
    driver = "oj"
    return "ok"'''