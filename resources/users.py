import models
from flask import Blueprint,request,jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

####### BLUEPRINT
users = Blueprint('users','users')

###### ROUTES

### -------- Get all Users -------- 
@users.route('/',methods=['GET'])
def get_users():
    users = models.User.select()
    user_dicts = [model_to_dict(user) for user in users]

    for user in user_dicts:
        user['created'] = str(user['created'])
    
    return jsonify(
        data=user_dicts,
        message=f"Successfully found {len(user_dicts)} users.",
        status=200
    ), 200

### -------- Create New User (Sign Up) -------- 
@users.route('/register',methods=['POST'])
def create_user():
    payload = request.get_json()
    
    #normalize data
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    print(payload) 

    try:
        models.User.get(models.User.email == payload['email'])
        # if no error is thrown, another user with the email already exists
        return jsonify(
            message='a user with that email already exists',
            status=401
        ),401
    except models.DoesNotExist:
        # If the does not exist error is thrown, the user email is not taken 
        # hash the password using bcrypt 
        print('user doesnt exist yet ...')
        password_hash = generate_password_hash(payload['password'])

        try:
            # if we get no error here the user name is also not taken 
            created_user = models.User.create(
                username=payload['username'],
                email=payload['email'],
                password=password_hash
            )

            login_user(created_user)

            print(created_user)

            created_user_dict = model_to_dict(created_user)
            # processing created_user_dict to be serializeable
            created_user_dict.pop('password')
            created_user_dict['created'] = str(created_user_dict['created'])
            
            return jsonify(
                data=created_user_dict,
                message=f"successfully created user {created_user_dict['username']}",
                status=201
            ),201
        except models.IntegrityError:
            # if we do get an error here then the username is taken
            return jsonify(
                message='That username is already taken',
                status=201
            ),201