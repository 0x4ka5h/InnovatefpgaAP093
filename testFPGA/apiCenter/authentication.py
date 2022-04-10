from flask import Blueprint, abort, jsonify, request, url_for
from itsdangerous import json
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from .model import User

auth = Blueprint('auth',__name__)

################################     signup    ####################################
@auth.route("/signup/"  , methods = ['POST'])
def singUp():

    type_ = request.json.get('type_')
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None or type_ is None:
        return "must provide username / password / type ^_^"

    if User.query.filter_by(type_=type_,username=username).first() is not None:
        return jsonify({"Reason ":str(username)+" already found under same role"})
    
    

    #if User.query.filter_by(username = username).first() is not None:
    #   abort(400) # existing user
    #user = User(username = username)
    #user.hash_password(password,method='sha256')
    #db.session.add(user)
    #db.session.commit()

    user = User(type_=type_,username = username,password=generate_password_hash(password, method='sha256'))
    # add the new user to the database
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'request': "success" ,"username" : username, "role":type_ }), 201
    #return "User added successfully"

#################################   login   #####################################
@auth.route("/Login/"  , methods = ['POST'])
def logIn():
    print(request.data)
    type_ = request.json.get('type_')
    username = request.json.get('username')
    password = request.json.get('password')

    if type_ is None:
        return jsonify({ 'request': "failed" ,"Reason" : "Please provide role/type_"}), 201


    user = User.query.filter_by(type_=type_,username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"request":"failed","Reason":"Double check role/username/password before submit"}),201
    else:
        login_user(user, remember=True)
        return jsonify({"request":"success"}),201

@auth.route("/ownerLogin/"  , methods = ['GET'])
def ownerLogIn():
    type_ = request.args['type_']
    username = request.args['username']
    password = request.args['password']
    
    if type_ is None:
        return jsonify({ 'request': "failed" ,"Reason" : "Please provide role/type_"}), 200


    user = User.query.filter_by(type_=type_,username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"request":"failed","Reason":"Double check role/username/password before submit"}),200
    else:
        login_user(user, remember=True)
        return jsonify({"request":"success"}),201

        
################################   logout   ######################################
@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return jsonify({"request":"successfull"})


