from marshmallow import fields, pre_load
from marshmallow.validate import Email, Length
from app.ext.serializer import BaseSchema

class UserSchema(BaseSchema):
    hidden_fields = ['password']

    email = fields.Str(required=True, validate=[Email()])
    username = fields.Str(required=True)
    password = fields.Str(required=True, validate=[Length(min=6)])

    @pre_load
    def pre_load_data(self, in_data, **kwargs):
        if in_data.get('email'):
            in_data['email'] = in_data['email'].lower().strip()        
        
        if in_data.get('username'):
            in_data['username'] = in_data['username'].lower().strip()

        if in_data.get('password'):
            in_data['password'] = in_data['password'].strip()
        return in_data
        

    class Meta:
        fields = ('id', 'created_at', 'email', 'username', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)