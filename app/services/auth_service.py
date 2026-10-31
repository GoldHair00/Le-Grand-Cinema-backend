from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app.errors import EmailAlreadyUsedError
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