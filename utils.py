from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from db import db
from models import Auditoria


def intentar_commit(user_id=None):
    db.session.info['user_id'] = user_id

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(
            500, message=f'Ocurrió un error en el servidor. Error: {str(e)}')


def log_audit_event(obj, operation, user_id, values_before={}, values_after={}):
    # Aquí puedes implementar la lógica para guardar el evento de auditoría en la base de datos
    # Por ejemplo:
    audit_entry = Auditoria(
        user_id=user_id,  # Asume que tienes una variable 'current_user' disponible
        tabla_origen=obj.__tablename__,
        registro_id=obj.id,
        operacion=operation,
        fecha=datetime.now(),
        valores_originales=values_before,
        valores_nuevos=values_after
    )
    db.session.add(audit_entry)
    # db.session.commit() // No hace falta y es preferible que dependa de un rollback general
