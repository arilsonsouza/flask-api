from datetime import timedelta

from flask import request, current_app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from marshmallow.exceptions import ValidationError
from sqlalchemy import or_

from app.api.utils import success_response, error_response, get_items_per_page, get_request_page
from app.api.v1.main import api_v1
from app.api.models import User
from app.api.v1.user.serializer import user_schema, users_schema
from app.ext.db import db

@api_v1.route('/users', methods=['GET'])
@jwt_required
def get_all_users():
    page = get_request_page(request)
    per_page = get_items_per_page(request, current_app)

    users = User.paginate(User.query.with_entities(
        User.id,
        User.email,
        User.username,
        User.created_at
    ).order_by(User.username.asc()), page, per_page, 'api_v1.get_all_users', users_schema)
    return success_response(users or [])

@api_v1.route('/users', methods=['POST'])
def store_a_user():
    
    try:        
        data = user_schema.load(request.json or {})
        return data
        
        email = data['email']
        username = data['username']

        user = User.query.filter(or_(User.email==email, User.username==username)).first()
        if user and user.email == email:
            return error_response(409, message=f'The email "{email}" is already being used')

        if user and user.username == username:
            return error_response(409, message=f'The username "{username}" is already being used')
        
        user = User(email=email, username=username)
        user.set_password(data['password'])

        
        user.save()
        result = user_schema.dump(user)
        return success_response(content=None, status_code=201, message=f'User {user.username} was successfully registered')
    except ValidationError as e:        
        return error_response(status_code=422, message=e.messages)    
    except BaseException as e:
        return error_response(status_code=422, message='Unable to register user')


@api_v1.route('/auth/login', methods=['POST'])
def authenticate_user():
    data = request.json or {}

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return error_response(404, 'User not found.')
    
    if not user.check_password(data['password']):
        return error_response(404, 'Incorrect password')
    
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
    return success_response(content={'access_token': access_token}, status_code=201, message='User logged successfully.')