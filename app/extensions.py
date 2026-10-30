from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
swagger = Swagger(template={
    "info": {"title": "Le Grand Cinéma API", "version": "1.0"},
    "securityDefinitions": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header", "description": "Format : Bearer <jeton>"}
    },
})
