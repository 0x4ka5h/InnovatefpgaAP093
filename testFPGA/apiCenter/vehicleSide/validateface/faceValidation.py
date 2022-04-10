import base64
from crypt import methods
from flask_login import login_required
from flask import Blueprint, jsonify, redirect, request, url_for
from ...model import vehicleDetails
from ... import db
import cv2
import json
from PIL import Image
import numpy as np
from . import validatingPerson, reConstructModel
faceValidationauth = Blueprint("faceValidationauth",__name__)

global dang
dang = 1


@faceValidationauth.route("/api/vehicle/ownerFriendValidation/", methods=['POST'])
#@login_required

def ownerFriendValidation():
    global dang
    data = request.json.get('validationImage')
    dec = base64.b64decode(data)
    nparr = np.fromstring(dec, np.uint8)
    image_ = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    #PIL_img=Image.open(image_).convert('L')
    #image_=np.array(PIL_img, 'uint8')
    #print(type(image_))

    validation_ = validatingPerson.predictTrustedPerson(image_)
    if validation_ == 1:
            f = open('apiCenter/ownerSide/alert.json','w+')
            data = {"isUnknown": 0,"isTowing": 0,"isDeclined": 0}
            json_object = json.dump(data,f)
            #f.write(json_object)
            f.close()

            f = open('apiCenter/ownerSide/choice.json','w+')
            data = {"allow": 1}
            json_object = json.dump(data,f)
            f.close()

            return "1"
    else:
        validation_ = validatingPerson.predictDeclinedPerson(image_)
        if validation_ == 1:
            f = open('apiCenter/ownerSide/alert.json','w+')
            data = {"isUnknown": 0,"isTowing": 0,"isDeclined": 1}
            json_object = json.dump(data,f)
            f.close()

            f = open('apiCenter/ownerSide/choice.json','w+')
            data = {"allow": -1}
            json_object = json.dump(data,f)
            f.close()
            return "0"
        else:
            cv2.imwrite("apiCenter/static/check/theft.png",image_)
            f = open('apiCenter/ownerSide/alert.json','w+')
            data = {"isUnknown": 1,"isTowing": 0,"isDeclined": 0}
            json_object = json.dump(data,f)
            f.close()

            f = open('apiCenter/ownerSide/choice.json','w+')
            data = {"allow": -1}
            json_object = json.dump(data,f)
            f.close()
            return "-1"
    




@faceValidationauth.route("/api/vehicle/validateThroughNotification/")
#@login_required

def validateThroughNotification():
    
    f = open('apiCenter/ownerSide/alert.json','r+')
    data  = json.load(f)
    f.close()
    
    return jsonify(data),200


@faceValidationauth.route("/api/vehicle/DataForNotification/")
@login_required

def DataForNotification():
    
    image = cv2.imread("apiCenter/static/check/theft.png")
    _,encoded = cv2.imencode('.png',image)
    base_encoded = base64.b64encode(encoded)
    print(1)
    return base_encoded,200

@faceValidationauth.route("/api/vehicle/AcceptanceORDecline/",methods=['POST'])
@login_required

def AcceptanceORDecline():

    choice = request.json.get('choice')
    if choice == 1:
        f = open('apiCenter/ownerSide/choice.json','w+')
        data = {"allow": 1}
        f.write(data)
        f.close()
        reConstructModel.addDataToTrustedPersons()
    else:
        f = open('apiCenter/ownerSide/choice.json','w+')
        data = {"allow": 0}
        f.write(data)
        f.close()
        reConstructModel.addDataToDeclinedPersons()
    
    return "0",200


@faceValidationauth.route("/api/vehicle/checkAcceptance/")
#@login_required

def checkAcceptance():
    f = open('apiCenter/ownerSide/choice.json','r+')
    data  = json.load(f)
    f.close()
    return jsonify(data),200

@faceValidationauth.route("/api/Towing/",methods=['POST'])
def Towing():
    k = request.json
    f = open('apiCenter/ownerSide/alert.json','r+')
    data  = json.load(f)
    data['isTowing'] = k['yn']
    f.close()

    f = open('apiCenter/ownerSide/alert.json','r+')
    json.dump(data,f)
    f.close()

    return jsonify(data),200