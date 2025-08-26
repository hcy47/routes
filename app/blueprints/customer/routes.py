from app.blueprints.customer import customers_bp
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, db



#create a customer route
@customers_bp.route('/', methods=['POST']) # the routes serve as the trigger  for ythe function below
def create_customer():
  try:
    data = customer_schema.load(request.json) # accesing the body of the request
  except ValidationError as e:
    return jsonify(e.messages), 400 # returning the error as a response so my clinent can see whats wrong

  new_customer = Customers(**data)
  db.session.add(new_customer)
  db.sesion.commit()
  return customer_schema.jsonify(new_customer), 201 # status code, succesfull creation

  # data = request.json # getting my customer data
  # new_customer = Customers(**data)  # Createc a customer object from my user data. (once translated data will be in the form of an dictionary)
  # db.session.add(new_customer) # adding customer to session
  # db.session.commit() # commit the session

#read customers
@customers_bp.route('', methods=['GET']) # end poijnt to get customer
def read_customers():
  customers = db.session.query(Customers).all()
  return customers_schema.jsonify(customers), 200 # ssucces 



# #Read Indivudual Customer - using dynamic endpoint
# @customers_bp.route('<int:customer_id>', methods=['GET'])
# def read_customer(customer_id):
#   customer = db.session.get(Customers, customer_id)
#   return customer_schema.jsonify(customer), 200


#delete A Customer
@customers_bp.route('<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
  customer = db.session.get(Customers, customer_id)
  db.session.delete(customer)
  db.session.commit()
  return jsonify({'message': f"Succesfully deleted{customer_id}"}), 200



#updating a customer
@customers_bp.route('<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
  customer = db.session.get(Customers, customer_id) # query for our customer to update
  if not customer: # checking if i got a customer
    return jsonify({"message": "User not found"}), 404 #if not return error message
  
  try:
    customer_data = customer_schema.load(request.json) # validating updates
  except ValidationError as e:
    return jsonify({'message': e.messages}), 400
  for key, value in customer_data.item(): # looping over atrributes and values from user data dictionary
    setattr(customer, key, value) # setting Object Attribute Value to replace
  db.session.commit()
  return customer_schema.jsonify(customer), 200
  

#   #query the user by id
#   #validate and deserialize the updateas that they are sending in the body if the request
#   #for each of the values that they are sending , we will change the value of the querried object
#   # commit the changes 
#   #return a response
