import models
from flask import Blueprint,request,jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user
import json
import decimal
from datetime import datetime

####### BLUEPRINT
climbs = Blueprint('climbs','climbs')

####### Custom JSON Encoders
class customEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, decimal.Decimal):
            return float(o)
        return json.JSONEncoder.default(self, o)

###### ROUTES

##########################################
### -------- Get all Climbs -------- 
##########################################
@climbs.route('/',methods=['GET'])
def get_climbs():
    climbs=models.Climb.select()
    climb_dicts=[model_to_dict(climb) for climb in climbs]

    climb_dicts = json.dumps(climb_dicts, cls=customEncoder, default=str)

    return jsonify(
        data=json.loads(climb_dicts),
        message=f"Successfully found {len(json.loads(climb_dicts))} climbs",
        status=200
    ),200


##########################################
### -------- Create New Climb -------- 
##########################################
@climbs.route('/',methods=['POST'])
def create_climb_log():
    payload=request.get_json()
    payload['creator']=current_user.id # logged in user is automatically the creator of the climb

    new_climb=models.Climb.create(**payload)
    climb_dict=model_to_dict(new_climb)

    climb_dict = json.dumps(climb_dict, cls=customEncoder, default=str)
    return jsonify(
        data=json.loads(climb_dict),
        message='Successfully created new climb',
        status=201
    ),201


##########################################
### ----- Get Current Users Climbs -------
##########################################
@climbs.route('/my_climbs',methods=['GET'])
def get_user_climbs():
    climb_dicts = [model_to_dict(climb) for climb in current_user.my_climbs]
    climb_dicts = json.dumps(climb_dicts,cls=customEncoder, default=str)
    climb_json = json.loads(climb_dicts)
    return jsonify(
        data=climb_json,
        message=f"Successfully found {len(climb_json)} climbs for user with id " + str(current_user.id),
        status=200
    ),200


##########################################
### -------- Show Climb -------- 
##########################################
@climbs.route('/<id>',methods=['GET'])
def get_climb(id):
    try:
        climb=models.Climb.get_by_id(id)

        climb_dict = json.dumps(model_to_dict(climb), cls=customEncoder, default=str)

        return jsonify(
            data=json.loads(climb_dict),
            message='Successfully found climb with id ' + id,
            status=200
        ),200
    except models.DoesNotExist:
        return jsonify(
            data={},
            message='Could not find climb with id ' + id,
            status=404
        ),404


##########################################
### -------- Edit Climb -------- 
##########################################
@climbs.route('/<id>', methods=['PUT'])
def edit_climb(id):
    payload=request.get_json()
    models.Climb.update(**payload).where(models.Climb.id==id).execute()

    climb_dict = json.dumps(model_to_dict(models.Climb.get_by_id(id)), cls=customEncoder, default=str)

    return jsonify(
        data=json.loads(climb_dict),
        message='Successfully updated climb with id ' + id,
        status=200
    ),200


##########################################
### -------- Delete Climb -------- 
##########################################
@climbs.route('/<id>', methods=['DELETE'])
def delete_climb(id):
    deleted_climb = models.Climb.get_by_id(id)
    models.Climb.delete_by_id(id)

    deleted_dict = json.dumps(model_to_dict(deleted_climb), cls=customEncoder, default=str)

    return jsonify(
        data=json.loads(deleted_dict),
        message='Successfully deleted climb with id ' + id, 
        status=200
    ),200