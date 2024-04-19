from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from schemas import StoreSchema, SQLAlchemyErrorSchema, ItemSchema
from models import StoreModel
from utils import intentar_commit


blp = Blueprint('Stores', __name__,
                description='Operaciones en Tiendas', url_prefix="/api")


@blp.route('/store')
class StoresAPI(MethodView):
    @blp.doc(description="Hace un query.all() sobre el Modelo Store", summary='Devuelve todos las Tiendas')
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.doc(description='Crea una tienda en la DB', summary='Crea una Tienda')
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    @blp.alt_response(500, schema=SQLAlchemyErrorSchema, description='SQLAlchemyError')
    def post(self, data):
        new_store = StoreModel(**data)

        db.session.add(new_store)
        intentar_commit()

        return new_store


@blp.route('/store/<int:store_id>')
class StoreAPI(MethodView):
    @blp.doc(description="Devuelve la información de una tienda por ID", summary='Devuelve una Tienda')
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id)


@blp.route('store/<int:store_id>/items')
class StoreItemsAPI(MethodView):
    @blp.doc(description='Devuelve los items de una tienda por ID', summary='Devuelve items de una tienda')
    @blp.response(200, ItemSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.items
