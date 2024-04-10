# sql schema models...

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

import webbrowser

from .database import Base, engine
from .schemas import ImageResponse

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

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.columns}


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
    file_name = Column(String)
    user_id = Column(Integer, ForeignKey(User.id))

    user = relationship("User", back_populates="images")
    tags = relationship("Tag", secondary=image_tag_association, back_populates="images")
    
    def to_dict(self):
        
        return {field.name: getattr(self, field.name) for field in self.__table__.columns}
    
    @property
    def url(self):
        # webbrowser.open_new(webbrowser.URL(f"file://{self.file_name}.jpg", "text".encode()))

        BASE_URL = "localhost:8000/images/"

        return BASE_URL + self.file_name
    
    def list_serialize(self):
        obj = ImageResponse(**self.to_dict(), url=self.url, user=self.user.to_dict())
        return obj.model_dump()
    

# map to Tag relation...
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    type = Column(String)
    # image_id = Column(Integer, ForeignKey("images.id"))

    images = relationship("Image", secondary=image_tag_association, back_populates="tags")

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.columns}



### Create tables if they don't exist
# mapper_registry.metadata.create_all(engine, checkfirst=True)

Base.metadata.create_all(engine)