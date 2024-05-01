from db import db

class TagModel(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    # Ver después si la relación está presente en el session objet, 
    # Para hacer obj.item.store.id