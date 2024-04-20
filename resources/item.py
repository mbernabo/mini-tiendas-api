from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    @jwt_required()
    def post(self, data):
        user_id = get_jwt_identity()
        tienda_user = StoreModel.query.get(data['store_id'])
        if not tienda_user:
            abort(404, message='Tienda no encontrada')

        if tienda_user.user_id != user_id:
            abort(401, message='No está autorizado a utilizar esta tienda')

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
