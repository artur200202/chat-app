from app import ma
from app.models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    """User schema for serialization"""
    class Meta:
        model = User
        load_instance = True
        include_fk = True

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)