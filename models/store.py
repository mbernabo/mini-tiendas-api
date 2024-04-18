from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    items = db.relationship(
        'ItemModel', back_populates='store', lazy='dynamic')
    
    owner = db.relationship('UserModel', back_populates='stores')
