from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app) #api object built on top of app object

class HelloWorld(Resource): #flask-restful classes inherit from resource
    def get(self):
        return {'about':'Hello World!'}
    
    def post(self):
        some_json = request.get_json()
        return some_json, 201

class Multi(Resource):
    def get(self, num):
        return {'result':num*10}

api.add_resource(HelloWorld,'/') #args = resource object and route
api.add_resource(Multi,'/multi/<int:num>')

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')

