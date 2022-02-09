from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'g00g1y5p4'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # blueprint for auth routes in our app
    from .authentication import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # home route and vehicleStatus route
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    ##########################    ownerSide        ###############################

    from apiCenter.ownerSide.apiGpsToOwner import ownerGPSauth
    app.register_blueprint(ownerGPSauth)



    ##########################    vehicleSide      ###############################
    from apiCenter.vehicleSide.apiGpsOfVehicle import vehicleGPSauth
    app.register_blueprint(vehicleGPSauth)

    from apiCenter.vehicleSide.validateface.faceValidation import faceValidationauth
    app.register_blueprint(faceValidationauth)

    from apiCenter.vehicleSide.validateface.reConstructModel import reConstructingAuth
    app.register_blueprint(reConstructingAuth)

    

    #############################   onRequests       #################################

    from apiCenter.onRequests.ownerCommands import ownerCommandsauth
    app.register_blueprint(ownerCommandsauth)

    from apiCenter.onRequests.cameraStream import cameraStreamauth
    app.register_blueprint(cameraStreamauth)

    from apiCenter.onRequests.remoteCommands import remoteCommandsauth
    app.register_blueprint(remoteCommandsauth)


    return app


















'''from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from authentication import auth
#app
app = Flask(__name__)
db = sqlalchemy(app)

#registers
app.register_blueprint(auth)

#database
app.config['SECRET_KEY'] = 'g00g1y5p4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

auth = HTTPBasicAuth()

users = {
    "a": generate_password_hash("a_"),
    "b": generate_password_hash("b_")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username



if __name__ == '__main__':
    app.run()'''