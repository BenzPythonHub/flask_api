from flask import Flask 
from flask_restful import Api
from resources.user import Users

app = Flask(__name__)
api = Api(app)


api.add_resource(Users, '/users')


@app.route('/')
def index():
    return "hello " + "123world XD"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)