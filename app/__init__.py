from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_mail import Mail
import flask 

db=SQLAlchemy()
loginmanager=LoginManager()
mail=Mail()

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    mail.init_app(app)
    loginmanager.init_app(app)
    config[config_name].init_app(app) # of course till now this is just a pass fucn
    # probably some more configs here
    from app.auth import auth as auth_blueprint
    from app.main import main as main_blueprint
    app.register_blueprint(auth_blueprint,url_prefix="/auth")
    app.register_blueprint(main_blueprint,url_prefix="/")
    # letting str be a func in jinja2 templates
    app.jinja_env.globals.update(str=str,len=len)
    from app.models import AnonymousUser
    #config for anon
    loginmanager.anonymous_user=AnonymousUser

    return app # tadaaah

 # this    
@loginmanager.unauthorized_handler
def unauth():
    return flask.redirect(flask.url_for('auth.login'))