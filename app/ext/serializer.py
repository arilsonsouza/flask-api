from flask_marshmallow import Marshmallow
from marshmallow import post_dump, validates_schema

ma = Marshmallow()

class BaseSchema(ma.Schema):
    hidden_fields = []

    @post_dump
    def remove_hidden_fields(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            if key not in self.hidden_fields
        }


    """Uncomment the function below to change the format of the error messages"""
    # def handle_error(self, exc, data, **kwargs):
    #     print('HANLE ERROR', exc.messages)
    #     messages = []
    #     for key, value in exc.messages.items():
    #         for index, message in enumerate(value):
    #             value[index] = f'{key}: {message}'
    #         messages.append({key: value})
        
    #     exc.messages = messages                

def init_app(app):
    ma.init_app(app)