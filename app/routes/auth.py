from flask import Blueprint, jsonify, request

from app.schemas.user import LoginSchema, RegisterSchema
from app.services import auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Créer un compte utilisateur
    ---
    tags:
      - Authentification
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [email, password, first_name, last_name]
          properties:
            email:
              type: string
              example: user@cinema.fr
            password:
              type: string
              example: MotDePasse123
            first_name:
              type: string
              example: Marie
            last_name:
              type: string
              example: Dupont
    responses:
      201:
        description: Compte créé
      409:
        description: Email déjà utilisé
      422:
        description: Données invalides
    """
    data = RegisterSchema().load(request.get_json(silent=True) or {})
    user = auth_service.register_user(**data)
    return jsonify({"id": user.id, "email": user.email, "role": user.role}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Se connecter et obtenir un jeton JWT
    ---
    tags:
      - Authentification
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [email, password]
          properties:
            email:
              type: string
              example: user@cinema.fr
            password:
              type: string
              example: MotDePasse123
    responses:
      200:
        description: Connexion réussie, jeton JWT renvoyé
      401:
        description: Email ou mot de passe incorrect
      422:
        description: Données invalides
    """
    data = LoginSchema().load(request.get_json(silent=True) or {})
    token, user = auth_service.login_user(**data)
    return jsonify({"access_token": token, "role": user.role}), 200