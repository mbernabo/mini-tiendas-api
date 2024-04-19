from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db
from schemas import ItemSchema, SQLAlchemyErrorSchema
from models import ItemModel, StoreModel
from utils import intentar_commit


blp = Blueprint('Items', __name__,
                description='Operaciones en Tiendas', url_prefix="/api")


@blp.route('/item')
class ItemAPI(MethodView):
    @blp.doc(description="Devuelve todos los items de Mini Tienda", summary='Devuelve todos las Items')
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.doc(description='Crea un item en la DB', summary='Crea un Item')
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    @jwt_required
    def post(self, data):

        StoreModel.query.get_or_404(data['store_id'])
        new_item = ItemModel(**data)

        db.session.add(new_item)
        intentar_commit()

        return new_item


@blp.route('item/<int:item_id>')
class ItemsApi(MethodView):
    @blp.doc(description='Devuelve la información de un item por ID', summary='Devuelve un item por ID')
    @blp.response(200, ItemSchema)
    def get(self):
        pass
