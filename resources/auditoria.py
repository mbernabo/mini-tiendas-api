from flask.views import MethodView
from flask_smorest import Blueprint
from models import Auditoria
from schemas import AuditoriaSchema
import json

blp = Blueprint('Auditoría', __name__,
                description='Guarda un registro de todas las operaciones CUD hechas en Store, Item o Tag', url_prefix="/api")


@blp.route('/auditoria')
class AuditTrail(MethodView):

    @blp.doc(description="Hace un query.all() sobre el Modelo Auditoría", summary='Devuelve todos las pistas de auditoría')
    @blp.response(200, AuditoriaSchema(many=True))
    def get(self):
        return Auditoria.query.all()
        
