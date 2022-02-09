'''from passlib.apps import custom_app_context as pwd_context
import sqlalchemy
from .__init__ import db

class User(db.Model):
    # ...
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)'''
from flask_login import UserMixin
from sqlalchemy import PrimaryKeyConstraint
from . import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    type_ = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class vehicleDetails(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    vehicleCode_ = db.Column(db.String(100))
    status_ = db.Column(db.String(100))
    timeStamp_ = db.Column(db.String(100),unique=True)
    driver_ = db.Column(db.String(100))
    mode_ = db.Column(db.String(100))
    gpsPointCurr_ = db.Column(db.String(100))

class ownerCommands(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    modeChange_ = db.Column(db.String(100))
    cameraView_ = db.Column(db.String(100))


class remoteControlValues(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    steerAngle_ = db.Column(db.Integer)
    breakFunc_ = db.Column(db.Integer)
    acccelarationFunc_ = db.Column(db.Integer)

class valuesForRemoteAccess(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    speed_ = db.Column(db.Integer)
    ultraSonicLeft_ = db.Column(db.Integer)
    ultraSonicRight_ = db.Column(db.Integer)
    ultraSonicBack1_ = db.Column(db.Integer)






