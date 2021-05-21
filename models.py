from logging import NullHandler
from peewee import *
import datetime
from flask_login import UserMixin 
 
DATABASE = SqliteDatabase('climbs.sqlite')

######## USERS MODEL ########
class User(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()
    display_name=CharField(null = True)
    description=CharField(null = True)
    is_admin=BooleanField(default=False)
    created=DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

######## ROUTES MODEL #######
class Route(Model):
    name=CharField(unique=True)
    location=CharField()
    description=CharField()
    image=BigBitField()
    created=DateTimeField(default=datetime.datetime.now)
    creator=ForeignKeyField(User, backref='my_routes')

    class Meta:
        database = DATABASE


########  CLIMBS MODEL ########
class Climb(Model):
    image=BigBitField() 
    created=DateTimeField(default=datetime.datetime.now)
    # creator=ForeignKeyField(User, backref='my_climbs')
    # route=ForeignKeyField(Route, backref='route_climbs')
    notes=CharField()
    climb_type=CharField()
    height=IntegerField()
    rating=CharField()
    performance=CharField()
    gym_outdoor=CharField()
    time=DecimalField()
    wall_type=CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User,Route,Climb], safe=True)
    print('connected to the database (and created tables if they weren\'t already there)')
    DATABASE.close()