from app import ma
from app.models import Room

class RoomSchema(ma.SQLAlchemyAutoSchema):
    """Room schema for serialization"""
    class Meta:
        model = Room
        load_instance = True
        include_fk = True


room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)