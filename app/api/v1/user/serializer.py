from app.ext.serializer import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'created_at', 'email', 'username')

user_schema = UserSchema()
users_schema = UserSchema(many=True)