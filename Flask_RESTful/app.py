from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [{'name': 'milk', 'price': 12.00}]

class Item(Resource):
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
