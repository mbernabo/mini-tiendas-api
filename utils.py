from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from db import db
from models import Auditoria, StoreModel, ItemModel, TagModel


def intentar_commit(user_id: int = None):
    """
    Intenta confirmar los cambios en la sesión de la base de datos y asigna el user_id proporcionado a la sesión.

    Args:
        user_id (int, opcional): El ID del usuario que está realizando la acción. Por defecto es None para contemplar los commits que no llevan control de auditoría

    Raises:
        HTTPException: Si se produce un error al intentar confirmar los cambios en la base de datos.

    """
    db.session.info['user_id'] = user_id

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(
            500, message=f'Ocurrió un error en el servidor. Error: {str(e)}')


def log_audit_event(obj, operation, user_id, values_before={}, values_after={}):
    tabla_origen = obj.__tablename__
    registro_id = obj.id

    registros_asociados_por_tabla_origen = {
        'stores': [None, None],
        'items': ['stores', obj.store_id],
        # 'tags': ['items', obj.item_id]
    }

    tabla_asociada, registro_asociado = registros_asociados_por_tabla_origen.get(tabla_origen)

    ultima_pista = Auditoria.query.filter_by(
        tabla_origen=tabla_origen, registro_id=registro_id).order_by(Auditoria.version.desc()).first()

    version = ultima_pista.version + 1 if ultima_pista else 1

    audit_entry = Auditoria(
        user_id=user_id,
        tabla_origen=tabla_origen,
        registro_id=registro_id,
        tabla_asociada=tabla_asociada,
        registro_asociado=registro_asociado,
        operacion=operation,
        fecha=datetime.now(),
        valores_originales=values_before,
        valores_nuevos=values_after,
        version=version
    )
    db.session.add(audit_entry)
    # db.session.commit() // No hace falta y es preferible que dependa de un rollback general


def seleccionarModelo(tabla_origen):
    tablas_modelos = {
        'stores': StoreModel,
        'items': ItemModel,
        'tags': TagModel
    }

    modelo = tablas_modelos.get(tabla_origen)

    return modelo
