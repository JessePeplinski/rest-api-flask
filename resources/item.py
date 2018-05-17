from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# inherits from resource
class Item(Resource): 

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank") # Look into JSON payload
    parser.add_argument('store_id', type=int, required=True, help="Every item need store id") # Look into JSON payload
     
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': 'Item now found'}, 404        

    def post(self,name):
        # IF (we've found an item and its not null, it matches the name)
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 # error checking for bad request

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "error occured inserting the item"}, 500 # server error

        return item.json(), 201 # created

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'item deleted'}
    
    def put(self,name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name) 

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()] }