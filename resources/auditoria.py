from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import Auditoria
from schemas import AuditoriaSchema
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint('Auditoría', __name__,
                description='Guarda un registro de todas las operaciones CUD hechas en Store, Item o Tag', url_prefix="/api")


@blp.route('/auditoria')
class AuditTrail(MethodView):

    @blp.doc(description="Hace un query.all() sobre el Modelo Auditoría", summary='Devuelve todos las pistas de auditoría')
    @blp.response(200, AuditoriaSchema(many=True))
    @jwt_required()
    def get(self):
        print(get_jwt())
        is_admin = get_jwt()['is_admin']
        if is_admin:
            return Auditoria.query.all()
        else:
            abort(401, message="No tiene privilegios para acceder a esta ruta")
