from app.blueprints.service_ticket import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Service_tickets, db, Mechanics
from app.blueprints.mechanic.schemas import mechanics_schema


@service_tickets_bp.route('', methods=['POST'])
def create_service_ticket():
  try:
    data = service_ticket_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages), 400
  
  new_service_ticket = Service_tickets(**data)
  db.session.add(new_service_ticket)
  db.session.commit()
  return service_ticket_schema.jsonify(new_service_ticket), 200


@service_tickets_bp.route('<int:service_ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(service_ticket_id, mechanic_id):
  service_ticket = db.session.get(Service_tickets, service_ticket_id)
  mechanic = db.session.get(Mechanics, mechanic_id)

  if mechanic not in service_ticket.mechanics:
    service_ticket.mechanics.append(mechanic) # creating relationship betwen service_tickets and mechanics
    db.session.commit()
    return jsonify({
      'message': f'succesfully added {mechanic.id} to service_ticket',
      'service_tickets': service_ticket_schema.dump(service_ticket), # use dump when tghe schema is adding just a piece of the return message
      'mechanics': mechanics_schema.dump(service_ticket.mechanics) # using  the boooks_schema to serialize the list of mechanics related to the service_tickets
    }), 200
  return jsonify("This mechanic is already on the service_ticket"), 400


@service_tickets_bp.route('<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(service_ticket_id, mechanic_id):
  service_ticket = db.session.get(Service_tickets, service_ticket_id)
  mechanic = db.session.get(Mechanics, mechanic_id)

  if mechanic in service_ticket.mechanics: # checking to see if the relationshipp still exist 
    service_ticket.mechanics.remove(mechanic) # removing relationship betwen service_tickets and mechanics
    db.session.commit()
    return jsonify({
      'message': f'succesfully removed {mechanic.id} from service_ticket',
      'service_tickets': service_ticket_schema.dump(service_ticket), # use dump when tghe schema is adding just a piece of the return message
      'mechanics': mechanics_schema.dump(service_ticket.mechanics) # using  the boooks_schema to serialize the list of mechanics related to the service_tickets
    }), 200
  
  return jsonify("This mechanic is not on the service_ticket anymore!"), 400
 






# retrieve all tickets
@service_tickets_bp.route('', methods=['GET'])
def retrive_all_tickets():
  service_tickets = db.session.query(Service_tickets).all()
  return service_tickets_schema.jsonify(service_tickets), 200