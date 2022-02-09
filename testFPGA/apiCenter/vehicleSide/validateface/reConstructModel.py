import base64
import os
import cv2
from flask_login import login_required
import numpy as np
from . import validatingPerson
from flask import Blueprint, jsonify, redirect, request, url_for

reConstructingAuth = Blueprint("reConstructingAuth",__name__)

def count_(dataTo):
    Tcount_ = len(os.listdir('apiCenter/vehicleSide/validateface/trustedPersons/'))
    Dcount_ = len(os.listdir('apiCenter/vehicleSide/validateface/declinedPersons/'))
    
    if dataTo==1:
        return Tcount_+1
    elif dataTo==0:
        return Dcount_+1

@reConstructingAuth.route("/api/vehicle/validateFace/adddataToTrustedPersons/", methods=['POST'])
@login_required
def addDataToTrustedPersons():
    data = request.json.get('imageData')
    count = request.json.get('count')
    if (count==1):
        c=count_(1)
        path = 'apiCenter/vehicleSide/validateface/trustedPersons/tp'+str(c)+"/"
        os.mkdir(path)

    dec = base64.b64decode(data)
    nparr = np.fromstring(dec, np.uint8)
    image_ = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    if (count<=10):
        path_to=path+str(count)+".png"
        cv2.imwrite(path_to,image_)
    return jsonify({"request":"successfull"})



@reConstructingAuth.route("/api/vehicle/validateFace/adddataToDeclineddPersons/", methods=['POST'])
@login_required
def addDataToDeclinedPersons():
    data = request.json.get('imageData')
    count = request.json.get('count')
    if (count==1):
        c=count_(1)
        path = 'apiCenter/vehicleSide/validateface/trustedPersons/dp'+str(c)+"/"
        os.mkdir(path)

    dec = base64.b64decode(data)
    nparr = np.fromstring(dec, np.uint8)
    image_ = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    if (count<=10):
        path_to=path+str(count)+".png"
        cv2.imwrite(path_to,image_)
    return jsonify({"request":"successfull"})




@reConstructingAuth.route("/api/vehicle/validateFace/reConstructModelToTrust/")
@login_required
def reConstructModelToTruste():
    validatingPerson.trainTrustedPersons()
    return jsonify({"request":"successfull"})




@reConstructingAuth.route("/api/vehicle/validateFace/reConstructModelToDecline/")
@login_required
def reConstructModelToTrusted():
    validatingPerson.trainDeclinedPersons()
    return jsonify({"request":"successfull"})