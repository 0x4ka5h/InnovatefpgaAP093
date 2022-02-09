from flask import Blueprint, jsonify
from . import db
from flask_login import login_required, current_user

main = Blueprint('main', __name__)



@main.route('/api/vehicleStatus')
def vehicleStatus():
    #username = request
    return jsonify({"vechileType":"car","status":"Status : Active"})

@main.route('/')
def home():
    try:
        return jsonify({"login":current_user.username,"message":" testing under AP093"})
    except:
        return jsonify({"login":"-----","message":" testing under AP093"})
