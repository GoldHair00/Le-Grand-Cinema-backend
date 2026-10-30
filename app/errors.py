from flask import jsonify
from marshmallow import ValidationError


class AppError(Exception):
    status_code = 400
    code = "bad_request"


class EmailAlreadyUsedError(AppError):
    status_code = 409
    code = "email_already_used"


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({"error": error.code, "message": str(error)}), error.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"error": "validation_error", "message": error.messages}), 422
