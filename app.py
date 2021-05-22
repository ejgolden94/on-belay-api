from flask import Flask
import os
from dotenv import load_dotenv
import models
from flask_login import LoginManager, login_manager
### Import resources
from resources.climbs import climbs
from resources.users import users
from resources.routes import routes

load_dotenv() # takes the environment variables from .env

DEBUG=True
PORT=8000

app= Flask(__name__)

######## Login Manager ###########
app.secret_key = os.environ.get("SECRET")
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return models.User.get_by_id(user_id)


######## Register Blueprints ###########
app.register_blueprint(climbs,url_prefix='/api/v1/climbs')
app.register_blueprint(users,url_prefix='/api/v1/users')
app.register_blueprint(routes,url_prefix='/api/v1/routes')

######## ROUTES ########

# TEST ROUTE
@app.route('/') 
def hello():
    return 'Hello, world!'

######## LISTENER ########
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)