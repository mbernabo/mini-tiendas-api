from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt, set_access_cookies, set_refresh_cookies, get_current_user

from db import db
from schemas import UserSchema, SQLAlchemyErrorSchema, LoginSchema, RefreshSchema
from models import UserModel
from utils import intentar_commit
from blocklist import BLOCKLIST

blp = Blueprint('Users', __name__,
                description='Operaciones con usuarios', url_prefix='/api')


# Solución al problema de los CORS
# @blp.after_request
# def after_request(response):
#     header = response.headers
#     header['Access-Control-Allow-Origin'] = 'http://localhost:5173'
#     header['Access-Control-Allow-Headers'] = 'Content-Type'
#     # Other headers can be added here if needed
#     return response


@blp.route('/user')
class UsersAPI(MethodView):

    @blp.doc(description="Devuelve los usuarios, con sus tiendas y productos", summary='Devuelve todos los Usuarios')
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @blp.doc(description='Crea un usuario', summary='Crea un usuario')
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    @blp.alt_response(500, schema=SQLAlchemyErrorSchema, description='SQLAlchemyError')
    def post(self, data):
        email_existente = UserModel.query.filter_by(
            email=data['email']).first()
        if email_existente:
            abort(400, message='Ya existe ese email en la base de datos')
        new_user = UserModel(**data)
        db.session.add(new_user)
        intentar_commit()
        return new_user


@blp.route('/login')
class UserLoginAPI(MethodView):
    @blp.doc(description="Loguea un usuario por email y contraseña", summary='Login del Usuario')
    @blp.arguments(UserSchema)
    @blp.response(200, LoginSchema)
    def post(self, data):
        user = UserModel.query.filter_by(email=data['email']).first()
        if user and user.password == data['password']:
            response = jsonify({'message:': 'Usuario logueado exitosamente'})
            access_token = create_access_token(identity=user.id, fresh=True)
            set_access_cookies(response, access_token)
            print(response.__dict__)
            return response
        else:
            abort(401, message='Credenciales inválidas')


@blp.route('/refresh')
class TokenRefreshAPI(MethodView):
    @blp.doc(description="Genera un non-fresh token", summary='Genera Non Fresh Tokens')
    @blp.response(201, RefreshSchema)
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        return {'access_token': new_token}


@blp.route('/logout')
class LogOutUser(MethodView):
    @blp.doc(description="Revoca el access y refresh token", summary='Desloguea a un usuario')
    @blp.response(200)
    @jwt_required(verify_type=False)
    def delete(self):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        BLOCKLIST.add(jti)

        return jsonify(mensaje=f'{ttype.capitalize()} token revocado')
