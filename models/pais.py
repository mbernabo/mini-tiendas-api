from db import db

class PaisModel(db.Model):
    __tablename__ = 'paises'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)