from app import ma
from app.models import Message
from marshmallow import fields

class MessageSchema(ma.SQLAlchemyAutoSchema):
    """Message schema for serialization"""
    
    author = fields.Nested('UserSchema', only=['id', 'username'])
    room = fields.Nested('RoomSchema', only=['id', 'name'])
    
    class Meta:
        model = Message
        load_instance = True
        include_fk = True


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)