from flask import jsonify, make_response
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

def success_response(content = [], status_code=200, message=None, success=True):
    payload = {
        'success': success,
        'content': content
    }

    if message:
        payload['message'] = message
    
    response = jsonify(payload)
    response.status_code = status_code
    return response

def error_response(status_code, message=''):
    payload = {        
        'error': str(status_code) + ' ' + HTTP_STATUS_CODES.get(status_code, 'Unknown error')
    }

    if isinstance(message, str):
        message = [message if message else 'There was an error in your request.']
    
    payload['message'] = [message]
    
    response = jsonify(payload)
    response.status_code = status_code
    return response

def error_handler(e):
    code = 500
    error, message = str(e).split(':', 1)
    
    if isinstance(e, HTTPException):
        code = e.code
    
    return make_response(jsonify(error=error), code)

def get_request_page(request):
    return request.args.get('page', 1, type=int)
    
def get_items_per_page(request, current_app):
    return min(request.args.get('per_page', int(current_app.config['PER_PAGE']), type=int), int(current_app.config['MAX_ITEMS_PER_PAGE']))