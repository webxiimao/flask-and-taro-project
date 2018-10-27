from apps.api.v1 import create_blueprint_v1
from apps.user.api import userRoute

def register_blueprints(app):
    app.register_blueprint(create_blueprint_v1(), url_prefix="/v1")
    app.register_blueprint(userRoute, url_prefix="/user")
