from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager


import os

from db import db

from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST


def create_app(db_url=None):
    app = Flask(__name__)

    CORS(app)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Mini Tiendas REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api-docs"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = '271474320750803842679971001457890860447'


    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "El token ha sido revocado.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Esta función agrega información al JWT. La verificación del Admin sería usando el identity(ID) recibido con el id del User en la DB
        if identity == 7:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "El token ha expirado.",
                    "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "La verificación de la firma falló.",
                    "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "El request no contiene un access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "Se requiere un fresh token en este endpoint.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    api = Api(app)

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
