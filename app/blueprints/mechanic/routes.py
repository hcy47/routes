from app.blueprints.mechanic import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema, login_schema
from flask import request, jsonify, render_template
from marshmallow import ValidationError
from app.models import Mechanics, db
from app.extensions import limiter
from app.utils.util import encode_token, token_required
from werkzeug.security import generate_password_hash, check_password_hash



@mechanics_bp.route('/login', methods=['POST'])
@limiter.limit('5 per 10 min')
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
@limiter.limit("5 per day")
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



@mechanics_bp.route('', methods=['GET'])
@limiter.limit('15 per hour')
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
@limiter.limit('5 per day')
@token_required
def delete_mechanic():
  token_id = request.mechanic_id # grabbing the token id from the request
 
  mechanic = db.session.get(Mechanics, token_id) #Query my user out of db
  db.session.delete(mechanic)
  db.session.commit()
  return jsonify({'message': f'Succesfully deleted{token_id}'}), 200
