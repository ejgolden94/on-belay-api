import models
from flask import Blueprint,request,jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

####### BLUEPRINT
users = Blueprint('users','users')

###### ROUTES
@users.toute('/',methods=['GET'])
def get_users():
    users = models.User.select()
    user_dicts = [model_to_dict(user) for user in users]

    for user in user_dicts:
        user['created'] = str(user['created'])
    
    return jsonify(
        data=user_dicts,
        message=f"Successfully fount {len(user_dicts)} users.",
        status=200
    ), 200