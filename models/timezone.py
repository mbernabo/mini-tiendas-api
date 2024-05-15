from db import db

class TzModel(db.Model):
    __tablename__ = 'timezones'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    # De usarlo, debería ser un String con 00:00, usarlo sólo si se consigue programáticamente ese dato cuando se buscan las tz's
    offset = db.Column(db.Integer, nullable=False)

    pais = db.Column(db.Integer, db.ForeignKey('paises.id'), nullable=False)

    

