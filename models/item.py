from db import db

class ItemModel(db.Model):
    __versioned__ = {}
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    description = db.Column(db.String)

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel', back_populates='items')
