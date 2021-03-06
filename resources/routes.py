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
### -------- Get all Routes ------------
# also this takes a query param of setting to get
# the only the outdoor or indoor routes
##########################################
@routes.route('/',methods=['GET'])
def get_routes():
    if not request.args.get('setting'): 
        routes = models.Route.select().order_by(models.Route.created.desc())
    else:
        routes = models.Route.select().where(models.Route.gym_outdoor == request.args.get('setting').capitalize()).order_by(models.Route.created.desc()).execute()
    route_dicts = [model_to_dict(route) for route in routes]
    # normalize unserializeable data
    route_dicts = json.dumps(route_dicts,cls=DateTimeEncoder, default=str)

    return jsonify(
        data=json.loads(route_dicts),
        message= f"Successfully found {len(json.loads(route_dicts))} routes",
        status=200
    ),200


##########################################
### --------- Create New Route ---------- 
##########################################
@routes.route('/',methods=['POST'])
def create_route():
    payload=request.get_json()
    payload['creator'] = current_user.id
    payload['gym_outdoor'] = payload['gym_outdoor'].capitalize()

    new_route= models.Route.create(**payload)

    # normalize unserializeable data
    new_route_dict = json.dumps(model_to_dict(new_route),cls=DateTimeEncoder, default=str)
    new_route_json = json.loads(new_route_dict)
    
    return jsonify (
        data = new_route_json,
        message = f"Successfully created new route, {new_route_json['name']}.",
        status=201
    ),201


##########################################
### ----- Get Current Users Routes -------
##########################################
@routes.route('/my_routes',methods=['GET'])
def get_user_routes():
    route_dicts = [model_to_dict(route) for route in current_user.my_routes]
    route_dicts = json.dumps(route_dicts,cls=DateTimeEncoder, default=str)
    route_json = json.loads(route_dicts)
    return jsonify(
        data=route_json,
        message=f"Successfully found {len(route_json)} routes for user with id " + str(current_user.id),
        status=200
    ),200

############################################
### ----- Get all of a Routes Climbs -------
# ------------------------------------------
# also this takes a query param of user to get
# the climb for a route for just that user id
# that param should just pass in a boolean 
############################################
@routes.route('<id>/climbs',methods=['GET'])
def get_routes_climbs(id):
    route = models.Route.get_by_id(id)
    if not request.args.get('user'):
        climb_dicts = [model_to_dict(climb) for climb in route.route_climbs]
    else:
        climbs = models.Climb.select().where((models.Climb.route==route.id) & (models.Climb.creator == current_user.id)).order_by(models.Climb.created.desc())
        climb_dicts = [model_to_dict(climb) for climb in climbs]

    climb_dicts = json.dumps(climb_dicts,cls=DateTimeEncoder, default=str)
    climb_json = json.loads(climb_dicts)
    return jsonify(
        data=climb_json,
        message=f"Successfully found {len(climb_json)} climbs for route with id " + id,
        status=200
    ),200

##########################################
### --------- Show Route ---------- 
##########################################
@routes.route('/<id>', methods=['GET'])
def get_route(id):
    try:
        route = models.Route.get_by_id(id)
        route_json = json.dumps(model_to_dict(route),cls=DateTimeEncoder)

        return jsonify(
            data=json.loads(route_json),
            message=f"Successfully found route with id " + id,
            status=200
        ),200
    except models.DoesNotExist:
        return jsonify(
            data={},
            message=f"Counld not find route with id " + id,
            status=404
        ),404


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