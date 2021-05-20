from peewee import *
import datetime
 
DATABASE = SqliteDatabase('climbs.sqlite')

######## USERS MODEL ########
class User(Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()
    display_name=CharField()
    description=CharField()
    is_admin=BooleanField()
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
    creator=ForeignKeyField(User, backref='my_climbs')
    route=ForeignKeyField(Route, backref='route_climbs')
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