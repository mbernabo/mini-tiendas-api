from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from db import db


class Auditoria(db.Model):
    __tablename__ = 'auditoria'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tabla_origen = db.Column(db.String, nullable=False)
    registro_id = db.Column(db.Integer, nullable=False)
    tabla_asociada = db.Column(db.String)
    registro_asociado = db.Column(db.Integer)
    operacion = db.Column(db.String, nullable=False)
    version = db.Column(db.Integer)
    # Para el proyecto se puede usar server_default que declara el default al momento de crear la tabla | Chequear el nullable, tampoco haría falta
    fecha = db.Column(db.DateTime(timezone=True),
                      nullable=False, default=func.now())
    comentarios = db.Column(db.String)
    valores_originales = db.Column(JSONB, nullable=False)
    valores_nuevos = db.Column(JSONB, nullable=False)
