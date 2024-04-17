from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError
from db import db


def intentar_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(
            500, message=f'Ocurrió un error en el servidor. Error: {str(e)}')
