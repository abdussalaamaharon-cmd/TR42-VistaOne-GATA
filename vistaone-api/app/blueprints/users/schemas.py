from app.extensions import ma
from app.models import User
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
    
    password = fields.String(load_only=True)  # accepts password on load but never returns it

user_schema = UserSchema()
users_schema = UserSchema(many=True)
login_schema = UserSchema(exclude=['name', 'phone', 'id'])