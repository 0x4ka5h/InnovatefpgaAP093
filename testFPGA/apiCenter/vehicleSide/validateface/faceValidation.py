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
            return redirect(url_for('validateThroughNotification',data))




@faceValidationauth.route("/api/vehicle/validateThroughNotification/")
@login_required

def validateThroughNotification(data):
    
    ## sending notification to phone with  imageData  ##
    ## need to write code ##

    #if accepts
    reConstructModel.addDataToTrustedPersons()

    #else
    reConstructModel.addDataToDeclinedPersons()
    
    
    return data
