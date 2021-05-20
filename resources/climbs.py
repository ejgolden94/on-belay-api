import models
from flask import Blueprint,request,jsonify
from playhouse.shortcuts import model_to_dict
import decimal
import json

####### BLUEPRINT
climbs = Blueprint('climbs','climbs')

###### ROUTES

## Index Route 
@climbs.route('/',methods=['GET'])
def get_climbs():
    climbs=models.Climb.select()
    print(climbs)
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


# New Climb Route
@climbs.route('/',methods=['POST'])
def create_climb_log():
    payload=request.get_json()
    new_climb=models.Climb.create(**payload)
    climb_dict=model_to_dict(new_climb)
    # popping image because its stored in bytes and is not serializeable
    climb_dict.pop('image')
    print(climb_dict)
    return jsonify(
        data=climb_dict,
        message='Successfully created new climb',
        status=201
    ),201