from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, get_jwt_identity, set_access_cookies
from dotenv import load_dotenv

import os

from db import db

from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST

load_dotenv()


def create_app(db_url=None):
    app = Flask(__name__)

    # Creo que no hace falta para el response, creo que sí.. Porque también lo uso en el after_request para manejar la renovación automática
    CORS(app, supports_credentials=True)
    # Segunda opción de CORS
    # CORS(app, origins=["http://localhost:5173"], headers=['Content-Type'],
    #      expose_headers=['Access-Control-Allow-Origin'], supports_credentials=True)
    # tercera
    # CORS(app, origins='http://localhost:5173', supports_credentials=True)

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
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    # Esto debe ir en True en PROD para que sea solo a a través de HTTPS
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    # Pruebas fucking cookies
    app.config['JWT_COOKIE_SAMESITE'] = 'None'
    # app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # True en Prod
    # app.config['CORS_EXPOSE_HEADERS'] = '*'

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

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(
                    identity=get_jwt_identity(), fresh=False)
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response

    return app
