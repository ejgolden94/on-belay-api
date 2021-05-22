import models
from flask import Blueprint, request, jsonify
from peewee import * 
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

####### BLUEPRINT
routes = Blueprint('routes','routes')

###### ROUTES

##########################################
### -------- Get all Routes -------- 
##########################################
@routes.route('/',method=['GET'])
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
@routes.route('/',method=['POST'])
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