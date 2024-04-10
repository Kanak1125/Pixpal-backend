# sql schema models...

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base, mapper_registry, engine

image_tag_association = Table (
    "image_tag_association",
    Base.metadata,
    Column("image_id", Integer, ForeignKey("images.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    profile_image_url = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    images = relationship("Image", back_populates="user")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    blur_hash = Column(String)
    created_at = Column(String)
    description = Column(String)
    alt_description = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    color = Column(String)
    likes = Column(Integer)
    # file_name = Column(String)
    user_id = Column(Integer, ForeignKey(User.id))

    user = relationship("User", back_populates="images")
    tags = relationship("Tag", secondary=image_tag_association, back_populates="images")

# map to Tag relation...
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    type = Column(String)
    # image_id = Column(Integer, ForeignKey("images.id"))

    images = relationship("Image", secondary=image_tag_association, back_populates="tags")


### Create tables if they don't exist
# mapper_registry.metadata.create_all(engine, checkfirst=True)

Base.metadata.create_all(engine)