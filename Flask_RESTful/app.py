from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'never_put_keys_in_source'

api = Api(app)

# Use the authentication and identity apps created in security file.  This will get a jwt token back
# authenticate
# identity 
jwt = JWT(app, authenticate, identity)

items = [{'name': 'milk', 'price': 12.00}]

class Item(Resource):
    # Decorator that we must do jwt authe
    @jwt_required()
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return {'item': name}
        return {'item': 'Item Not Found'}, 404


    def post(self, name):
            # The get_json() call requires the header type to be set properly
            parameters = request.get_json()
            item = {'name':parameters['name'], 'price':parameters['price']}
            items.append(item)
            return item


class Items(Resource):
    def get(self):
        return jsonify({'items': items})

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port=5000, debug=True)
