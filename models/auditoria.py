from sqlalchemy.dialects.postgresql import JSONB

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
    fecha = db.Column(db.DateTime, nullable=False)
    comentarios = db.Column(db.String)
    valores_originales = db.Column(JSONB, nullable=False)
    valores_nuevos = db.Column(JSONB, nullable=False)
