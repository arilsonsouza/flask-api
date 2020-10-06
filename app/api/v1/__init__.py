from app.api.v1.main import api_v1
from app.api.v1.user import resources

def init_app(app):
    app.register_blueprint(api_v1, url_prefix='/api/v1')