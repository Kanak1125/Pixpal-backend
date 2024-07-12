import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .utils import parse_env
parse_env()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
db = os.getenv("DB_NAME")

# connection_string...
SQLALCHEMY_DATABASE_URL = "postgresql://{0}:{1}@{2}/{3}".format(user, password, host, db)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# create a top level Session configuration...
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# map the class to the db records by inheriting the class by the orm model...

# create a base class from which all mapped classes should inherit...
Base = declarative_base()