from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemas import ItemSchema, SQLAlchemyErrorSchema
from models import ItemModel
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
    def post(self, data):
        new_item = ItemModel(**data)

        db.session.add(new_item)
        intentar_commit()

        return new_item
