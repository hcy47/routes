from app.extensions import ma
from app.models import Mechanics


class MechanicsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics #Creates a schema that validates the data as defined by our Mechanics Model

mechanic_schema = MechanicsSchema() 
mechanics_schema = MechanicsSchema(many=True) #Allows this schema to translate a list of Mechanics objects all at once
