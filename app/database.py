from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = "postgres"
password = "KanakPost1"
host = "localhost"
db = "image_gallery_db"

# connection_string...
SQLALCHEMY_DATABASE_URL = "postgresql://{0}:{1}@{2}/{3}".format(user, password, host, db)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# create a top level Session configuration...
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# map the class to the db records by inheriting the class by the orm model...
Base = declarative_base()