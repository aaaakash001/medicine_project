import os


class Config:
    DATABASE_PROTOCOL = "postgresql"
    DATABASE_USER = "docassist"
    DATABASE_PASSWORD = "aakashchaitanya"
    DATABASE_HOST = "localhost"
    DATABASE_PORT = "5432"
    DATABASE_NAME = "medicine"

    SQLALCHEMY_DATABASE_URI = f'{DATABASE_PROTOCOL}://' \
        + f'{DATABASE_USER}:{DATABASE_PASSWORD}' \
        + f'@{DATABASE_HOST}:{DATABASE_PORT}' + f'/{DATABASE_NAME}'
    SECRET_KEY = ']0c@$$^[_by_@@4@$6c6@^[@n7@'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


if os.environ.get('FLASK_ENV') == 'production':
    app_config = ProductionConfig
else:
    app_config = DevelopmentConfig
