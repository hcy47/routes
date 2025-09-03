from app.blueprints.mechanic import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema, login_schema
from flask import request, jsonify, render_template
from marshmallow import ValidationError
from app.models import Mechanics, db
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required
from werkzeug.security import generate_password_hash, check_password_hash



@mechanics_bp.route('/login', methods=['POST'])
def login():
  try:
    data = login_schema.load(request.json) #send email and pasword
  except ValidationError as e:
    return jsonify(e.messages), 400 # returning error as  a reponse so my cllient can see whats wrong
  
  mechanic = db.session.query(Mechanics).where(Mechanics.email == data['email']).first() # search my db for user with the passed in email

  if mechanic and check_password_hash(mechanic.password, data['password']): # check the user stored password  hash against the password that was sent
    token = encode_token(mechanic.id)
    return jsonify({
      "message": f"Succesfully Loggid in {mechanic.first_name}",
      "auth_token":token
    }), 200
  else:
    return jsonify({'messages': "Invalid email or password"}), 403


#create mechanic
@mechanics_bp.route('', methods=['POST'])
# @limiter.limit("5 per day")
def create_mechanic():
  try:
    data = mechanic_schema.load(request.json)
  except ValidationError as e :
    return jsonify(e.messages), 400
  
  data['password'] = generate_password_hash(data['password'])

  new_mechanic = Mechanics(**data)
  db.session.add(new_mechanic)
  db.session.commit()
  return ('Adding New Mechanic')


#read
@mechanics_bp.route('', methods=['GET'])
@limiter.limit('40 per hour')
@cache.cached(timeout=60)
def read_mechanic():
  mechanics = db.session.query(Mechanics).all()
  return mechanics_schema.jsonify(mechanics), 200




@mechanics_bp.route('<int:mechanic_id>', methods=['PUT'])
@limiter.limit('1 per month')
@token_required
def update_mechanic(mechanic_id):
  mechanic = db.session.get(Mechanics, mechanic_id)
  if not mechanic:
    return jsonify({'message':"Mechanic not found"}), 400
  
  try:
    mechanic_data = mechanic_schema.load(request.json)
  except ValidationError as e :
    return jsonify({"message": e.messages}), 400
  for key, value in mechanic_data.items():
    setattr(mechanic, key, value)
  db.session.commit()
  return mechanic_schema.jsonify(mechanic), 200
  


@mechanics_bp.route('', methods=['DELETE'])
@limiter.limit('50 per day')
@token_required
def delete_mechanic():
  token_id = request.mechanic_id # grabbing the token id from the request
 
  mechanic = db.session.get(Mechanics, token_id) #Query my user out of db
  db.session.delete(mechanic)
  db.session.commit()
  return jsonify({'message': f'Succesfully deleted{token_id}'}), 200


@mechanics_bp.route("/most_ticket", methods=['GET'])
def get_ticket_mechanics():
  mechanics = db. session.query(Mechanics).all() #grabbing all mechanics

  # sort mechanics based on how mani=y tickets they have been the part of
  mechanics.sort(key=lambda mechanic: len(mechanic.service_tickets), reverse=True)

  output = []
  for mechanic in mechanics[:3]:
    serviced_tickets = {
      "mechanic": mechanic_schema.dump(mechanic), #translate the mechanic to json
      "service_tickets": len(mechanic.service_tickets) #add the emount of the service tickets
    }
    output.append(serviced_tickets) # add this dict. to an output

  return mechanics_schema.jsonify(mechanics[:3])






  # lambda num1, num2: num1 + num2