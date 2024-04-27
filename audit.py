from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import json
# from db import db
from models import StoreModel, ItemModel, TagModel, Auditoria
from utils import log_audit_event


def register_audit_events(db):
    @event.listens_for(db.session, 'after_flush')
    def after_flush(session, flush_context):
        user_id = session.info.get('user_id')
        for obj in session.new:
            if isinstance(obj, (StoreModel, ItemModel, TagModel)):
                operation = 'CREATE'
                values = json.dumps({c.name: getattr(obj, c.name)
                                    for c in obj.__table__.columns})
                log_audit_event(obj, operation, user_id, {}, values)

        for obj in session.dirty:
            if isinstance(obj, (StoreModel, ItemModel, TagModel)):
                operation = 'UPDATE'
                values_before = json.dumps(
                    {c.name: getattr(obj, '_previous_%s' % c.name) for c in obj.__table__.columns})
                values_after = json.dumps(
                    {c.name: getattr(obj, c.name) for c in obj.__table__.columns})
                log_audit_event(obj, operation, user_id,
                                values_before, values_after)

        for obj in session.deleted:
            if isinstance(obj, (StoreModel, ItemModel, TagModel)):
                operation = 'DELETE'
                values = json.dumps({c.name: getattr(obj, c.name)
                                    for c in obj.__table__.columns})
                log_audit_event(obj, operation, user_id, values, {})
