from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.customer import customers_bp
from .blueprints.mechanic import mechanics_bp
from .blueprints.service_ticket import service_tickets_bp
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs'
API_URL ='/static/swagger.yaml'


#creating swagger blueprint
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Mechanic Management API'})


def create_app(config_name):

    app = Flask(__name__) #Creating base app
    app.config.from_object(f'config.{config_name}')


    #initialize extensions (plugging them in)
    #adding db to the app
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    #Register blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    return app