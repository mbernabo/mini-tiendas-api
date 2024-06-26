from marshmallow import Schema, fields, validate, validates, ValidationError
import re

fields.Field.default_error_messages["required"] = "Este campo es obligatorio"

error_messages = {
    'length': 'El contenido del campo debe tener entre {min} y {max} caracteres',
    'email': '{input} no es un email válido',

}


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(
        min=3, max=70, error=error_messages['length']))
    description = fields.Str(required=True)
    user_id = fields.Int(dump_only=True)


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(
        min=3, max=70, error=error_messages['length']))
    price = fields.Float(required=True)
    description = fields.Str()
    store_id = fields.Int(required=True)

    @validates('price')
    def validate_price(self, value):
        message = 'El campo precio puede tener un máximo dos decimales'
        pattern = r'^\d+(\.\d{1,2})?$'
        # Paso a string el float que viene de JSON para aplicarle la RE
        value_str = str(value)
        if not re.search(pattern, value_str):
            raise ValidationError(message)


class ItemSchema(PlainItemSchema):
    # store_id = fields.Int(required=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class SearchItem(Schema):
    q = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=validate.Email(
        error=error_messages['email']))
    password = fields.String(
        required=True, load_only=True, validate=validate.Length(
            min=8, error="La contraseña debe tener al menos {min} caracteres.")
    )

    stores = fields.List(fields.Nested(StoreSchema()), dump_only=True)

    # Validación personalizada para comprobar que todas las expresiones regulares coincidan en cualquier parte de la cadena
    @validates('password')
    def validate_password(self, value):
        patterns = [
            (r'[A-Z]', "La contraseña debe contener al menos una letra mayúscula."),
            (r'[a-z]', "La contraseña debe contener al menos una letra minúscula."),
            (r'\d', "La contraseña debe contener al menos un dígito."),
            (r'[!@#$%^&*(),.?":{}|<>]',
             "La contraseña debe contener al menos un carácter especial.")
        ]
        for pattern, message in patterns:
            if not re.search(pattern, value):
                raise ValidationError(message)


class SQLAlchemyErrorSchema(Schema):
    code = fields.Int()
    message = fields.Str()
    status = fields.Str()


# Estos en realidad no hacen falta porque son solo dump y no son objetos, aunque sirven para la documentación
# Saco el dump only porque sólo los uso para Response


class SimpleLoginSchema(Schema):
    user_id = fields.Int()
    email = fields.Str()


class LoginSchema(SimpleLoginSchema):
    access_token = fields.Str()
    refresh_token = fields.Str()


class CheckAdminSchema(Schema):
    is_admin = fields.Bool()


class RefreshSchema(Schema):
    access_token = fields.Str()


class SimpleAuditoriaSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    tabla_origen = fields.Str()
    operacion = fields.Str()
    version = fields.Int()
    # Ver después que ya podría formatear la fecha desde acá - Hecho
    fecha = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    fecha_tz = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    comentarios = fields.Str()
    valores_originales = fields.Raw()
    valores_nuevos = fields.Raw()


class AuditoriaSchema(SimpleAuditoriaSchema):
    tabla_origen = fields.Str()
    registro_id = fields.Int()
    tabla_asociada = fields.Str()
    registro_asociado = fields.Int()


class DetailedAuditoriaSchema(Schema):
    nombre_usuario = fields.Str()
    nombre_original_tienda = fields.Str()
    fecha_creacion = fields.Str()
    pista_id = fields.Int()
