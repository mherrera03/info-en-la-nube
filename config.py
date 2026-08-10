import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")

    # Render entrega la URL como "postgres://", SQLAlchemy 1.4+ requiere "postgresql://"
    _db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tienda_musica_dev")
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
