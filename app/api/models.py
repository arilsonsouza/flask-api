import jwt

from time import time

from flask import current_app, url_for
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from app.ext.db import db

class BaseModel(db.Model):
    __abstract__ = True

    _hidden_fields = ['created_at', 'updated_at']

    @classmethod
    def get(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def get_by(cls, **kw):
        return cls.query.filter_by(**kw).first()

    def before_save(self, *args, **kwargs):
        pass

    def after_save(self, *args, **kwargs):
        pass

    def save(self, commit=True):
        self.before_save()
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

        self.after_save()
    
    def before_update(self, *args, **kwargs):
        pass

    def after_update(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        self.before_update(*args, **kwargs)
        try:
            db.session.commit()
            self.after_update(*args, **kwargs)            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()     

    @staticmethod
    def paginate(query, page, per_page, endpoint, model_schema, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': model_schema.dump(resources.items),
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
				'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
				'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }
        return data

    def __repr__(self):
        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys() if n not in self._hidden_fields)
        return "%s(%s)" % (self.__class__.__name__, values)

class User(BaseModel):
    __abstract__ = False
    __tablename__ = 'users'
    _hidden_fields = ['created_at', 'updated_at', 'password']

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False, unique=True, index=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)    
    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode()

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms='HS256'
            )['reset_password']
        except Exception as e:
            return
        return User.query.get(id)
   