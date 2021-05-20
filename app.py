from flask import Flask
import models

DEBUG=True
PORT=8000

app= Flask(__name__)

######## ROUTES ########

# TEST ROUTE
@app.route('/') 
def hello():
    return 'Hello, world!'

######## LISTENER ########
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)