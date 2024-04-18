from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from schemas import UserSchema, SQLAlchemyErrorSchema
from models import UserModel
from utils import intentar_commit

blp = Blueprint('Users', __name__,
                description='Operaciones con usuarios', url_prefix='/api')


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
        email_existente = UserModel.query.filter_by(email=data['email']).first()
        if email_existente:
            abort(400, message='Ya existe ese email en la base de datos')
        new_user = UserModel(**data)
        db.session.add(new_user)
        intentar_commit()
        return new_user
