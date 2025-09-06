from app.blueprints.inventory import inventorys_bp
from .schemas import inventory_schema, inventorys_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Inventory, db
from app.extensions import limiter, cache

#create
@inventorys_bp.route('/', methods= ['POST'])
@limiter.limit('500 per day')
def create_inventory():

  try:
    data = inventory_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages), 400 
  

  new_inventory = Inventory(**data)
  db.session.add(new_inventory)
  db.session.commit()
  return inventory_schema.jsonify(new_inventory), 201


#read inventory
@inventorys_bp.route("/", methods=["GET"])
def read_inventorys():
  inventorys = db.session.query(Inventory).all() # end point to get inventory
  return inventorys_schema.jsonify(inventorys), 200 # succes





#update an inventory
@inventorys_bp.route("/<int:inventory_id>", methods=["PUT"])
def update_inventory(inventory_id):
  inventory = db.session.get(Inventory, inventory_id)
  if not inventory:
    return jsonify({"message": "Inventory not found"}), 404
  
  try:
    inventory_data = inventory_schema.load(request.json)
  except ValidationError as e:
    return jsonify({"message": e.messages}), 400
  
  for key, value in inventory_data.items():
    setattr(inventory, key, value)
    
  db.session.commit()
  return inventory_schema.jsonify(inventory), 200





#delete
@inventorys_bp.route("/<int:inventory_id>", methods=["DELETE"])
def delete_inventory(inventory_id):
  inventory = db.session.get(Inventory, inventory_id)
  db.session.delete(inventory)
  db.session.commit()
  return jsonify({"message": f"SUccesfullly deleted {inventory_id}"}), 200

