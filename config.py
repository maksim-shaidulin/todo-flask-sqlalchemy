import os

_db_user = os.environ['POSTGRES_USER']
_db_password = os.environ['POSTGRES_PASSWORD']
_db_host = os.environ['POSTGRES_HOST']
_db_name = os.environ['POSTGRES_DB']
_db_port = os.environ['POSTGRES_PORT']

DATABASE_URI = f'postgresql+psycopg2://{_db_user}:{_db_password}@{_db_host}:{_db_port}/{_db_name}'
