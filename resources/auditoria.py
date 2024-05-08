from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
import simplejson as json
from sqlalchemy import or_

from schemas import AuditoriaSchema, DetailedAuditoriaSchema, SimpleAuditoriaSchema
from models import Auditoria, UserModel
from utils import seleccionarModelo


blp = Blueprint('Auditoría', __name__,
                description='Guarda un registro de todas las operaciones CUD hechas en Store, Item o Tag', url_prefix="/api")


@blp.route('/auditoria')
class AuditTrails(MethodView):

    @blp.doc(description="Hace un query.all() sobre el Modelo Auditoría", summary='Devuelve todos las pistas de auditoría')
    @blp.response(200, AuditoriaSchema(many=True))
    @jwt_required(fresh=True)
    def get(self):
        is_admin = get_jwt()['is_admin']
        if is_admin:
            return Auditoria.query.order_by(Auditoria.fecha).all()
        else:
            abort(401, message="No tiene privilegios para acceder a esta ruta")


@blp.route('/auditoria/tiendas')
class AuditTiendas(MethodView):
    @blp.doc(description="Hace un query con filtro operación Create y Version 1", summary='Devuelve las tablas en su momento de creación')
    @blp.response(200, DetailedAuditoriaSchema(many=True))
    @jwt_required()
    def get(self):
        is_admin = get_jwt()['is_admin']
        if is_admin:
            resultados = Auditoria.query.filter(
                Auditoria.operacion == 'CREATE', Auditoria.version == 1, Auditoria.tabla_origen == 'stores').order_by(Auditoria.fecha).all()
            data = []
            if not resultados:
                abort(
                    404, message='No se encontraron tablas que cumplan los criterios de búsqueda')
            for resultado in resultados:
                tienda = {}
                # store = StoreModel.query.get(resultado.registro_id)
                # Eso tiene un problema, que es que la tienda ya pudo haber sido borrada
                valores_nuevos = json.loads(resultado.valores_nuevos)
                user = UserModel.query.get(valores_nuevos['user_id'])
                tienda['nombre_usuario'] = user.email
                tienda['nombre_original_tienda'] = valores_nuevos['name']
                tienda['fecha_creacion'] = resultado.fecha
                tienda['pista_id'] = resultado.id
                data.append(tienda)
            return data
        else:
            abort(401, message="No tiene privilegios para acceder a esta ruta")


@blp.route('/auditoria/pista/<int:pista_id>')
class AuditTrail(MethodView):
    @blp.doc(description='Devuelve la historia de auditoría de una Tienda desde la creación - versión 1', summary='Devuelve la historia completa de una Tienda')
    @blp.response(200, SimpleAuditoriaSchema(many=True))
    @jwt_required(fresh=True)
    def get(self, pista_id):
        is_admin = get_jwt()['is_admin']
        if is_admin:
            pista = Auditoria.query.get_or_404(pista_id)
            # Usar la tabla_origen y tabla_asociada garantiza que sea el registro correcto,
            # Pero en el caso de 'stores' no tienen tabla asociada. Ver como resolver.
            # Edit: le pongo 'items' por defecto a 'stores' ya que es la única correspondencia.

            if pista.tabla_origen == 'stores':
                eventos_por_fecha = Auditoria.query.filter(
                    or_(
                        (Auditoria.tabla_origen == pista.tabla_origen) & (
                            Auditoria.registro_id == pista.registro_id),
                        (Auditoria.tabla_origen == pista.tabla_asociada) & (
                            Auditoria.registro_asociado == pista.registro_id)
                    )
                ).order_by(Auditoria.fecha).all()

                return eventos_por_fecha
            else:
                abort(
                    400, message='En esta ruta sólo se permite procesar pistas de Auditoría de Tiendas')
        else:
            abort(401, message='No tiene privilegios para acceder a esta ruta')
