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

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    profile_image_url: str
    email: str

class UserCreate(UserBase):
    password: str

# Don't return password of the user, so inherit from the UserBase...
class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class ImageBase(BaseModel):
    blur_hash: str
    created_at: datetime
    description: str | None = None
    alt_description: str | None  = None
    width: int
    height: int
    color: str
    file_name: str
    likes: int

class ImageCreate(ImageBase):
    tags: list[Tag]

class ImageResponse(ImageBase):
    id: int
    url: str
    user: User

# now instance of Image will contain its id, and the tags associated with it...
class Image(ImageBase):
    id: int
    user: User
    # tags: list[Tag] = []

    class Config:
        orm_mode = True