# sql schema models...

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

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

    tags = relationship("Tag", back_populates="images")

# map to Tag relation...
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    type = Column(String)

    images = relationship("Image", back_populates="tags")