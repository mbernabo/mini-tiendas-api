from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemas import StoreSchema, SQLAlchemyErrorSchema
from models import StoreModel
from utils import intentar_commit


blp = Blueprint('Stores', __name__,
                description='Operaciones en Tiendas', url_prefix="/api")


@blp.route('/store')
class StoreAPI(MethodView):
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
