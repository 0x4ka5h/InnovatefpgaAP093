import base64
import cv2,numpy as np
from sqlalchemy import text
from flask_login import login_required
from flask import Blueprint, jsonify, redirect, request, url_for
from ..model import ownerCommands
from .. import db

cameraStreamauth = Blueprint("cameraStreamauth",__name__)

@cameraStreamauth.route("/api/stream/cameraStreamByOwner/",methods=['POST'])
@login_required
def cameraStreamByOwner():

    camIndex_ = request.json.get('camIndex')

    if int(camIndex_) == 1:
        image = cv2.imread("apiCenter/static/1/view.png")
        _,encoded = cv2.imencode('.png',image)
        base_encoded = base64.b64encode(encoded)
        print(1)
        return base_encoded
    elif int(camIndex_) == 2:
        image = cv2.imread("apiCenter/static/2/view.jpg")
        _,encoded = cv2.imencode('.png',image)
        base_encoded = base64.b64encode(encoded)
        print(2)
        return base_encoded


@cameraStreamauth.route("/api/stream/cameraStreamFromVehicle/",methods=['POST'])
@login_required
def cameraStreamFromVehicle():

    camIndex_ = request.json.get('camIndex')
    imageData = request.json.get('imageData')
    if int(camIndex_) == 1:
        dec = base64.b64decode(imageData)
        nparr = np.fromstring(dec, np.uint8)
        image_ = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite("apiCenter/static/1/view.png",image_)
        return jsonify({"request":"successfull"}),201

    elif int(camIndex_) == 2:
        dec = base64.b64decode(imageData)
        nparr = np.fromstring(dec, np.uint8)
        image_ = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite("apiCenter/static/2/view.png",image_)
        return jsonify({"request":"successfull"}),201