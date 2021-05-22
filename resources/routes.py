import models
from flask import Blueprint, request, jsonify
from peewee import * 
from playhouse.shortcuts import model_to_dict
from flask_login import current_user
from datetime import datetime 
import json

####### BLUEPRINT
routes = Blueprint('routes','routes')

####### Custom JSON Encoders
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

###### ROUTES

##########################################
### -------- Get all Routes -------- 
##########################################
@routes.route('/',methods=['GET'])
def get_routes():
    routes = models.Route.select()
    route_dicts = [model_to_dict(route) for route in routes]
    # normalize unserializeable data
    for route in route_dicts:
        route['created'] = str(route['created'])    
        route.pop('image')

    return jsonify(
        data=route_dicts,
        message= f"Successfully found {len(route_dicts)} routes",
        status=200
    ),200

##########################################
### --------- Create New Route ---------- 
##########################################
@routes.route('/',methods=['POST'])
def create_route():
    payload=request.get_json()
    payload['creator'] = current_user.id

    new_route= models.Route.create(**payload)

    new_route_dict = model_to_dict(new_route)
    # normalize unserializeable data
    new_route_dict.pop('image')
    new_route_dict['created'] = str(new_route_dict['created'])
    
    return jsonify (
        data = new_route_dict,
        message = f"Successfully created new route, {new_route_dict['name']}."
    )


##########################################
### --------- Edit Route ---------- 
##########################################
@routes.route('/<id>',methods=['PUT'])
def edit_route(id):
    payload=request.get_json()
    models.Route.update(**payload).where(models.Route.id == id).execute()
    edited_route = models.Route.get_by_id(id)
    edited_dict = json.dumps(model_to_dict(edited_route),cls=DateTimeEncoder)

    return jsonify(
        data=json.loads(edited_dict),
        message=f"successfully edited route with id " + id,
        status=200 
    ),200


##########################################
### --------- Delete Route ---------- 
##########################################
@routes.route('/<id>', methods=['DELETE'])
def delete_route(id):
    delete_route = models.Route.get_by_id(id)
    models.Route.delete_by_id(id)
    delete_route = json.dumps(model_to_dict(delete_route),cls=DateTimeEncoder)

    return jsonify(
        data=json.loads(delete_route),
        message= f"Succesfully deleted route with id " + id,
        status=200
    ),200