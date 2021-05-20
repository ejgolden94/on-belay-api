from flask import Flask
import models
### Import resources
from resources.climbs import climbs

DEBUG=True
PORT=8000

app= Flask(__name__)

######## Register Blueprints
app.register_blueprint(climbs,url_prefix='/api/v1/climbs')

######## ROUTES ########

# TEST ROUTE
@app.route('/') 
def hello():
    return 'Hello, world!'

######## LISTENER ########
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)