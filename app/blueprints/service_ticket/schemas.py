from app.extensions import ma
from app.models import Service_tickets


class Service_ticketsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_tickets #Creates a schema that validates the data as defined by our Service_tickets Model
        include_fk = True

service_ticket_schema = Service_ticketsSchema() 
service_tickets_schema = Service_ticketsSchema(many=True)