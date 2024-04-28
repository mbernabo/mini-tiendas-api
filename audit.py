from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm.attributes import get_history
import simplejson as json
# from db import db
from models import StoreModel, ItemModel, TagModel
from utils import log_audit_event


def register_audit_events(db):
    @event.listens_for(db.session, 'before_flush')
    def before_flush(session, flush_context, instances):
        for obj in session.dirty:
            if isinstance(obj, (StoreModel, ItemModel, TagModel)):
                # get_history devuelve el primer elemento de la lista de objetos borrados para un atributo
                # sólo si el attr tuvo cambios, sino, devuelve el valor original
                obj._previous_values = {
                    c.name: (
                        get_history(obj, c.name).deleted[0] if get_history(obj, c.name).has_changes()
                        else get_history(obj, c.name).unchanged[0]
                    )
                    for c in obj.__table__.columns
                }

    @event.listens_for(db.session, 'after_flush')
    def after_flush(session, flush_context):
        user_id = session.info.get('user_id')

        for obj in session.new:
            if isinstance(obj, (StoreModel, ItemModel, TagModel)):
                operation = 'CREATE'
                values = json.dumps({c.name: getattr(obj, c.name)
                                    for c in obj.__table__.columns})
                log_audit_event(obj, operation, user_id, None, values)

        for obj in session.dirty:
            if isinstance(obj, (StoreModel, ItemModel, TagModel)):
                operation = 'UPDATE'
                values_before = json.dumps(
                    getattr(obj, '_previous_values', {}))
                values_after = json.dumps(
                    {c.name: getattr(obj, c.name) for c in obj.__table__.columns})
                log_audit_event(obj, operation, user_id,
                                values_before, values_after)

        for obj in session.deleted:
            if isinstance(obj, (StoreModel, ItemModel, TagModel)):
                operation = 'DELETE'
                values = json.dumps({c.name: getattr(obj, c.name)
                                    for c in obj.__table__.columns})
                log_audit_event(obj, operation, user_id, values, None)
