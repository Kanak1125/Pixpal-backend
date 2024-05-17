# sql schema models...

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, backref

from .database import Base, engine, SessionLocal
from .schemas import ImageResponse, TagResponse

image_tag_association = Table (
    "assoc_image_tag",
    Base.metadata,
    Column("image_id", Integer, ForeignKey("images.id"), primary_key= True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key= True)
)

session = SessionLocal()


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
    # images = relationship("Image", back_populates="users")

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.columns}

class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True, index=True)
    hue = Column(Integer)
    saturation = Column(Integer)
    value = Column(Integer)

    images = relationship("Image", back_populates="average_color")

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
    likes = Column(Integer)
    file_name = Column(String)
    average_color_id = Column(Integer, ForeignKey('colors.id'), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    
    tags = relationship("Tag", secondary="assoc_image_tag", back_populates="images")

    average_color = relationship("Color", back_populates="images", lazy="joined")

    user = relationship("User", back_populates="images", lazy="joined")
    
    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.columns}
    
    @property
    def url(self):
        BASE_URL = "http://localhost:8000/images/"

        return {
            'small': BASE_URL + self.file_name,
            'regular': BASE_URL + self.file_name,
            'large': BASE_URL + self.file_name
        }
    
    def list_serialize(self):
        tags = [{
            "id": tag.id, 
            "title": tag.title, 
            "type": tag.type
            } for tag in self.tags]

        obj = ImageResponse(**self.to_dict(), urls=self.url, user=self.user.to_dict(), average_color=self.average_color.to_dict(), tags=tags)
        return obj.model_dump()
    

# map to Tag relation...
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    type = Column(String)
    # image_id = Column(Integer, ForeignKey("images.id"))

    # images = relationship("ImageTag", back_populates="tags")
    images = relationship("Image", secondary="assoc_image_tag", back_populates="tags")
    
    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.columns}
    
    def list_serialize(self):
        images_id = [image.id for image in self.images]

        obj = TagResponse(**self.to_dict(), images=images_id)
        return obj.model_dump()


### Create tables if they don't exist
Base.metadata.create_all(engine)