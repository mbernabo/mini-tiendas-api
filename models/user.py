from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    # En el proyecto original lleva 256 para guardar el Hash
    password = db.Column(db.String(60), nullable=False)
    perfil = db.Column(db.String(50)) # Not Null en el proyecto original

    stores = db.relationship(
        'StoreModel', back_populates='owner', lazy='dynamic')
