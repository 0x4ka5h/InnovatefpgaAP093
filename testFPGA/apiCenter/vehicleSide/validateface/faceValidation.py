import base64
from crypt import methods
from flask_login import login_required
from flask import Blueprint, jsonify, redirect, request, url_for
from ...model import vehicleDetails
from ... import db
import cv2
import numpy as np
from . import validatingPerson, reConstructModel
faceValidationauth = Blueprint("faceValidationauth",__name__)

dang = 0


@faceValidationauth.route("/api/vehicle/ownerFriendValidation/", methods=['POST'])
@login_required

def ownerFriendValidation():
    
    data = request.json.get('validationImage')
    dec = base64.b64decode(data)
    nparr = np.fromstring(dec, np.uint8)
    image_ = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    #print(type(image_))

    validation_ = validatingPerson.predictTrustedPerson(image_)

    if validation_ >= 85:
            return "Ok"
    else:
        validation_ = validatingPerson.predictDeclinedPerson(image_)
        if validation_ >= 85:
            return "Block"
        else:
            dang = 1
            cv2.imwrite("theft.png",image_)
            return 




@faceValidationauth.route("/api/vehicle/validateThroughNotification/")
@login_required

def validateThroughNotification():
    
    data = {'isthreat':dang}

    #if accepts
    #reConstructModel.addDataToTrustedPersons()

    #else
    #reConstructModel.addDataToDeclinedPersons()
    
    return jsonify(data),200


@faceValidationauth.route("/api/vehicle/DataForNotification/")
@login_required

def DataForNotification():
    
    image = cv2.imread("apiCenter/static/check/theft.png")
    _,encoded = cv2.imencode('.png',image)
    base_encoded = base64.b64encode(encoded)
    print(1)
    return base_encoded

@faceValidationauth.route("/api/vehicle/AcceptanceORDecline/")
@login_required

def AcceptanceORDecline():

    choice = request.json.get('choice')
    if choice == 1:
        reConstructModel.addDataToTrustedPersons()
    else:
        reConstructModel.addDataToDeclinedPersons()
    
    return "0",200
