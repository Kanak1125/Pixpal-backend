from pydantic import BaseModel

from datetime import datetime


class TagBase(BaseModel):
    title: str
    type: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    images: str

    class Config:
        orm_mode = True

class ImageBase(BaseModel):
    blur_hash: str
    created_at: datetime
    description: str
    alt_description: str
    width: int
    height: int
    color: str
    likes: int

class ImageCreate(ImageBase):
    pass

# now instance of Image will contain its id, and the tags associated with it...
class Image(ImageBase):
    id: int
    tags: list[Tag] = []

    class Config:
        orm_mode = True