from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.errors import EmailAlreadyUsedError, InvalidCredentialsError
from app.extensions import db
from app.models import User


def register_user(email, password, first_name, last_name):
    user = User(
        email=email.lower(),
        password_hash=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name,
    )
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise EmailAlreadyUsedError("Cet email est déjà utilisé")
    return user

def login_user(email, password):
    user = User.query.filter_by(email=email.lower()).first()
    if user is None or not check_password_hash(user.password_hash, password):
        raise InvalidCredentialsError("Email ou mot de passe incorrect")
    token = create_access_token(identity=str(user.id),
                                additional_claims={"role": user.role})
    return token, user