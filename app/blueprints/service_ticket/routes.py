from app.blueprints.service_ticket import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Service_tickets, db


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


@service_tickets_bp.route('<int:ticket_id>/<int:mechanic_id>', methods=['PUT']):
def assign_mechanic():
  pass


#retrieve all tickets
# @service_tickets_bp.route('', methods=['GET'])
# def retrive_all_tickets():
#   service_tickets = db.session.query(Service_tickets).all()
#   return service_tickets_schema.jsonify(service_tickets), 200