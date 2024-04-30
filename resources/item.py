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
        tienda_user = StoreModel.query.get_or_404(data['store_id'])

        if tienda_user.user_id != user_id:
            abort(401, message='No está autorizado a utilizar esta tienda')

        new_item = ItemModel(**data)

        db.session.add(new_item)
        intentar_commit(user_id)

        return new_item


@blp.route('item/<int:item_id>')
class ItemsApi(MethodView):
    @blp.doc(description='Devuelve la información de un item por ID', summary='Devuelve un item por ID')
    @blp.response(200, ItemSchema)
    def get(self):
        pass

    @blp.doc(description='Permite editar la información de un item por ID', summary='Edita un item por ID')
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    @jwt_required()
    def put(self, data, item_id):
        user_id = get_jwt_identity()
        item = ItemModel.query.get_or_404(item_id)
        if item.store.user_id == user_id:
            # Reviso si el item pertenece al store que envía el cliente:
            if item.store_id == data.get('store_id'):
                # Establezco los nuevos valores de los atributos de item
                for key, value in data.items():
                    setattr(item, key, value)
            else:
                abort(400, message='El item solicitado no pertenece a esta tienda')
        else:
            abort(401, message='No está autorizado a modificar este item')

        intentar_commit(user_id)
        return item

    @blp.doc(description='Borra un item por ID', summary='Borra un item por ID')
    @blp.response(200, description='Borrado exitoso', example={'message': 'Item borrado de forma exitosa'})
    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        user_id = get_jwt_identity()
        if item.store.user_id == user_id:
            db.session.delete(item)
            intentar_commit(user_id)
            return {'message': 'Item borrado de forma exitosa'}
        else:
            abort(401, message='No tiene derechos para realizar esta acción')
