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
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    
    tags = relationship("Tag", secondary="assoc_image_tag", back_populates="images")

    user = relationship("User", back_populates="images", lazy="joined")
    
    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.columns}
    
    @property
    def url(self):
        BASE_URL = "http://localhost:8000/"

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

        obj = ImageResponse(**self.to_dict(), urls=self.url, user=self.user.to_dict(), tags=tags)
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

    # images = relationship("Image", secondary="assoc_image_tag", backref='tags', lazy='dynamic')

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.columns}
    
    def list_serialize(self):
        images_id = [image.id for image in self.images]

        obj = TagResponse(**self.to_dict(), images=images_id)
        return obj.model_dump()


### Create tables if they don't exist

# mapper_registry.metadata.create_all(engine, checkfirst=True)
Base.metadata.create_all(engine)


# tag1 = Tag(id=202, title="water", type="search")
# tag2 = Tag(id=304, title="old", type="search")

# image1 = Image(id= 101, blur_hash='skdjf3jj33r3', created_at="some data", description= "lskjdfklj", alt_description= "ksjdfk", width=234, height= 800, color= "#ff0023", likes= 123, file_name="abc.jpg", tags=[tag1, tag2])

# session.add_all([tag1, tag2, image1])
# session.commit()