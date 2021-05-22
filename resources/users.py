import models
from flask import Blueprint,request,jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
import json 
from datetime import datetime

####### BLUEPRINT
users = Blueprint('users','users')

####### Custom JSON Encoders
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

###### ROUTES

##########################################
### -------- Get all Users -------- 
##########################################
@users.route('/',methods=['GET'])
def get_users():
    users = models.User.select()
    user_dicts = [model_to_dict(user) for user in users]

    user_dicts = json.dumps(user_dicts, cls=DateTimeEncoder, default=str)
    
    return jsonify(
        data=json.loads(user_dicts),
        message=f"Successfully found {len(json.loads(user_dicts))} users.",
        status=200
    ), 200

####################################################
### -------- Create New User (Sign Up) -------- 
####################################################
@users.route('/register',methods=['POST'])
def create_user():
    payload = request.get_json()
    
    #normalize data
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()

    try:
        models.User.get(models.User.email == payload['email'])
        # if no error is thrown, another user with the email already exists
        return jsonify(
            data={},
            message='a user with that email already exists',
            status=401
        ),401
    except models.DoesNotExist:
        # If the does not exist error is thrown, the user email is not taken 
        # hash the password using bcrypt 
        password_hash = generate_password_hash(payload['password'])

        try:
            # if we get no error here the user name is also not taken 
            created_user = models.User.create(
                username=payload['username'],
                email=payload['email'],
                password=password_hash
            )

            login_user(created_user)

            created_user_dict = model_to_dict(created_user)
            # processing created_user_dict to be serializeable
            created_user_dict.pop('password')
            created_user_dict= json.dumps(created_user_dict, cls=DateTimeEncoder, default=str)
            created_user_json=json.loads(created_user_dict)
            
            return jsonify(
                data=created_user_json,
                message=f"successfully created user {created_user_json['username']}",
                status=201
            ),201
        except models.IntegrityError:
            # if we do get an error here then the username is taken
            return jsonify(
                data={},
                message='That username is already taken',
                status=201
            ),201

################################
### -------- Login User -------- 
################################
@users.route('/login',methods=['POST'])
def login():
    payload = request.get_json()
    
    #normalize data
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()

    try:
        # does the user exist?
        user = models.User.get(models.User.email == payload['email'])
        user_dict=model_to_dict(user)
        # if no error is thrown the user exists and we can check their password
        password_match = check_password_hash(user_dict['password'], payload['password'])

        if password_match:
            # log in the user
            login_user(user)
            
            user_dict.pop('password')
            user_json=json.loads(json.dumps(user_dict,cls=DateTimeEncoder,default=str))
            
            return jsonify(
                data=user_json,
                message=f"Successfully logged in user {user_json['email']}",
                status=200
            ),200
        else:
            print('Incorrect Password')
            return jsonify(
                data={},
                message="Incorrect Username or Password",
                status=401
            ),401

    except models.DoesNotExist:
        # if theres an error the user wasnt found
        print('Username is incorrect')
        return jsonify(
            data={},
            message='Incorrect Username or Password',
            status=401
        ),401


################################
### ------- Logout User --------
################################
@users.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(
        data={},
        message='Successfully Logged Out User',
        status=200
    ),200