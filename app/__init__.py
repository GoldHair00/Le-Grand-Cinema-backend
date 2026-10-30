from flask import Flask

from app.config import Config
from app.errors import register_error_handlers
from app.extensions import db, jwt, swagger


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    register_error_handlers(app)

    from app.routes.auth import auth_bp
    from app.routes.health import health_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app
