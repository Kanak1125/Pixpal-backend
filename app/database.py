from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = "host"
password = ""
host = "postgresserver"
db = "image_gallery.db"

SQLALCHEMY_DATABASE_URL = "postgresql://{0}/{1}@{2}/{3}".format(user, password, host, db)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()