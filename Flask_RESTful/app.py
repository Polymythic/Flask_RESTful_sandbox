from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
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

    def delete(self, name):
        # There is some squirreliness with scope of the items.  Without referencing the global var
        # it assumes that the variable has local scope
        global items
        items = list(filter(lambda x: x['name']!= name, items))  
        return {"message": "Item deleted: {}".format(name)}

    def put(self, name):
        parser = reqparse.RequestParser()
        #This will look at the json payload 
        parser.add_argument("price", 
            type=float,
            required=True,
            help="This field cannot be left blank")
        parameters = parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            #This was not what was taught, but lets try it
            self.post(name)
        else:
            item.update(parameters)
        return item

class Items(Resource):
    def get(self):
        return jsonify({'items': items})

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(port=5000, debug=True)
