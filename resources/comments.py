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



