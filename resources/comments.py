import models
from flask import Blueprint,request,jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user
import json
from datetime import datetime

####### BLUEPRINT
comments = Blueprint('comments','comments')

####### Custom JSON Encoders
class customEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

###### ROUTES

##########################################
### -------- Get all Route Comments ------
##########################################
@comments.route('/route_comments/<route_id>',methods=['GET'])
def get_route_comments(route_id):
    try: 
        route = models.Route.get_by_id(route_id)
        comment_dicts = [model_to_dict(comment) for comment in route.route_comments.order_by(models.Comment.created.desc())]
        comment_dicts = json.dumps(comment_dicts,cls=customEncoder, default=str)
        comment_json = json.loads(comment_dicts)
        return jsonify(
            data=comment_json,
            message=f"Successfully found {len(comment_json)} comments for route with id " + str(route_id),
            status=200
        ),200
    except models.DoesNotExist:
        return jsonify(
            data={},
            message=f"Could not find route with id " + str(route_id),
            status=404
        ),404


##########################################
### -------- Create New Comment -------- 
##########################################
@comments.route('/',methods=['POST'])
def create_comment():
    payload=request.get_json()
    payload['creator']=current_user.id # logged in user is automatically the creator of the comment

    new_comment=models.Comment.create(**payload)
    comment_dict=json.dumps(model_to_dict(new_comment), cls=customEncoder, default=str)

    return jsonify(
        data=json.loads(comment_dict),
        message='Successfully created new comment',
        status=201
    ),201

##########################################
### -------- Edit Comment -------- 
##########################################
@comments.route('/<id>', methods=['PUT'])
def edit_comment(id):
    payload=request.get_json()
    models.Comment.update(**payload).where(models.Comment.id==id).execute()

    comment_dict = json.dumps(model_to_dict(models.Comment.get_by_id(id)), cls=customEncoder, default=str)

    return jsonify(
        data=json.loads(comment_dict),
        message='Successfully updated comment with id ' + id,
        status=200
    ),200

##########################################
### -------- Delete Comment -------- 
##########################################
@comments.route('/<id>', methods=['DELETE'])
def delete_comment(id):
    deleted_comment = models.Comment.get_by_id(id)
    models.Comment.delete_by_id(id)

    deleted_dict = json.dumps(model_to_dict(deleted_comment), cls=customEncoder, default=str)

    return jsonify(
        data=json.loads(deleted_dict),
        message='Successfully deleted comment with id ' + id, 
        status=200
    ),200
