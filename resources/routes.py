import models
from flask import Blueprint, request, jsonify
from peewee import * 
from playhouse.shortcuts import model_to_dict

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

    