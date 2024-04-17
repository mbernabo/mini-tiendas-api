from marshmallow import Schema, fields, validate


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(
        min=3, max=70, error='El nombre de la tienda debe tener entre 3 y 70 caracteres.'))
    description = fields.Str(required=True)


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(
        min=3, max=70, error='El nombre del item debe tener entre 3 y 70 caracteres.'))
    price = fields.Float(required=True)
    description = fields.Str()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class SQLAlchemyErrorSchema(Schema):
    code = fields.Int()
    message = fields.Str()
    status = fields.Str()
