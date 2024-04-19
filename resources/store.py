from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from schemas import StoreSchema, SQLAlchemyErrorSchema, ItemSchema
from models import StoreModel
from utils import intentar_commit


blp = Blueprint('Stores', __name__,
                description='Operaciones en Tiendas', url_prefix="/api")


@blp.route('/stores')
class StoresAPI(MethodView):
    @blp.doc(description="Hace un query.all() sobre el Modelo Store", summary='Devuelve todos las Tiendas')
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.doc(description='Crea una tienda en la DB', summary='Crea una Tienda')
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    @blp.alt_response(500, schema=SQLAlchemyErrorSchema, description='SQLAlchemyError')
    @jwt_required()
    def post(self, data):
        user_id = get_jwt_identity()
        new_store = StoreModel(user_id=user_id, **data)

        db.session.add(new_store)
        intentar_commit()

        return new_store


@blp.route('/store')
class StoreAPI(MethodView):
    @blp.doc(description="Devuelve las tiendas por User ID", summary='Devuelve las tiendas del Usuario')
    @blp.response(200, StoreSchema(many=True))
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return StoreModel.query.filter_by(user_id=user_id).all()


@blp.route('/store/<int:store_id>')
class StoreAPI(MethodView):
    @blp.doc(description="Devuelve la información de una tienda por ID", summary='Devuelve una Tienda')
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id)


@blp.route('/store/<int:store_id>/items')
class StoreItemsAPI(MethodView):
    @blp.doc(description='Devuelve los items de una tienda por ID', summary='Devuelve items de una tienda')
    @blp.response(200, ItemSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.items
