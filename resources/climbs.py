import models
from flask import Blueprint,request,jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user
import json
from datetime import datetime

####### BLUEPRINT
climbs = Blueprint('climbs','climbs')

####### Custom JSON Encoders
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


###### ROUTES

##########################################
### -------- Get all Climbs -------- 
##########################################
@climbs.route('/',methods=['GET'])
def get_climbs():
    climbs=models.Climb.select()
    climb_dicts=[model_to_dict(climb) for climb in climbs]

    for climb in climb_dicts:
        climb.pop('image')
        climb["created"] = str(climb["created"])
        climb["time"]= float(climb["time"])

    return jsonify(
        data=climb_dicts,
        message=f"Successfully found {len(climb_dicts)} climbs",
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

    climb_dict = json.dumps(climb_dict, cls=DateTimeEncoder)
    return jsonify(
        data=json.loads(climb_dict),
        message='Successfully created new climb',
        status=201
    ),201


##########################################
### -------- Show Climb -------- 
##########################################
@climbs.route('/<id>',methods=['GET'])
def get_climb(id):
    climb=models.Climb.get_by_id(id)

    climb_dict=model_to_dict(climb)
    
    climb_dict.pop('image')
    climb_dict["created"] = str(climb_dict["created"])
    climb_dict["time"]= float(climb_dict["time"])

    return jsonify(
        data=climb_dict,
        message='Successfully found climb with id ' + id,
        status=200
    ),200


##########################################
### -------- Edit Climb -------- 
##########################################
@climbs.route('/<id>', methods=['PUT'])
def edit_climb(id):
    payload=request.get_json()
    models.Climb.update(**payload).where(models.Climb.id==id).execute()
    climb_dict = model_to_dict(models.Climb.get_by_id(id))

    climb_dict.pop('image')
    climb_dict["created"] = str(climb_dict["created"])
    climb_dict["time"]= float(climb_dict["time"])

    return jsonify(
        data=climb_dict,
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

    deleted_dict = model_to_dict(deleted_climb)
    deleted_dict.pop('image')
    deleted_dict["created"] = str(deleted_dict["created"])
    deleted_dict["time"]= float(deleted_dict["time"])

    return jsonify(
        data=deleted_dict,
        message='Successfully deleted climb with id ' + id, 
        status=200
    ),200