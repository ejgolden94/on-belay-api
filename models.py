import os
from peewee import *
from playhouse.db_url import connect
import datetime
from flask_login import UserMixin 

DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///climbs.sqlite')

######## USERS MODEL ########
class User(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()
    display_name=CharField(null = True)
    avatart=CharField(null = True)
    description=TextField(null = True)
    is_admin=BooleanField(default=False)
    created=DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

######## ROUTES MODEL #######
class Route(Model):
    name=CharField() 
    location=CharField(null = True)
    height=IntegerField()
    rating=CharField()
    wall_type=CharField(null = True)
    description=TextField(null = True)
    protection=TextField(null = True)
    announcement=CharField(null = True)
    gym_outdoor=CharField()
    image=CharField(null = True) ## if we want to put multiple images here, we may want to rework this as an array
    created=DateTimeField(default=datetime.datetime.now)
    creator=ForeignKeyField(User, backref='my_routes')

    class Meta:
        database = DATABASE


########  CLIMBS MODEL ########
class Climb(Model):
    image=CharField(null = True)
    created=DateTimeField(default=datetime.datetime.now)
    creator=ForeignKeyField(User, backref='my_climbs')
    route=ForeignKeyField(Route, backref='route_climbs')
    notes=TextField(null = True)
    climb_type=CharField()
    performance=CharField()
    time=DecimalField(null = True)

    class Meta:
        database = DATABASE

########  COMMENTS MODEL ########
class Comment(Model):
    creator=ForeignKeyField(User, backref='my_comments')
    created=DateTimeField(default=datetime.datetime.now)
    route=ForeignKeyField(Route, backref='route_comments')
    text=CharField()
    rating=IntegerField(null = True)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User,Route,Climb,Comment], safe=True)
    print('connected to the database (and created tables if they weren\'t already there)')
    DATABASE.close()