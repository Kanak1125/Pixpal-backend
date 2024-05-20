from pydantic import BaseModel
from datetime import datetime
import colorsys

class URL(BaseModel):
    small: str
    regular: str
    large: str

class Color(BaseModel):
    hue: int
    saturation: int
    value: int
    
class ColorCreate(BaseModel):
    R: int
    G: int
    B: int

    def to_hsv(self):
        number_of_decimals = 4
        hsvColor = colorsys.rgb_to_hsv(
            round(self.R / float(256), number_of_decimals), 
            round(self.G / float(256), number_of_decimals),
            round(self.B / float(256), number_of_decimals)
        )# returns hsv in decimal...


        # de-normalize
        hue = int(hsvColor[0] * 360)
        saturation = int(hsvColor[1] * 100)
        value = int(hsvColor[2] * 100)

        localdict = locals() # get the local variables as dict key-value pairs...
        kwords = ("hue", "saturation", "value")
        data = { kword: localdict[kword] for kword in kwords}

        return Color(**data)

class TagBase(BaseModel):
    title: str
    type: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    
    class Config:
        orm_mode = True

class TagResponse(TagBase):
    id: int
    images: list[int]

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

# class ImageFormData (BaseModel):
#     description: str
#     color: str
#     tags: list[str]

class ImageBase(BaseModel):
    blur_hash: str
    created_at: datetime
    description: str | None = None
    alt_description: str | None  = None
    width: int
    height: int
    file_name: str
    likes: int

class ImageCreate(ImageBase):
    average_color: Color
    tags: list[int] = []

class ImageResponse(ImageCreate):
    id: int
    urls: URL
    user: User
    tags: list[Tag] = []

# now instance of Image will contain its id, and the tags associated with it...
class Image(ImageBase):
    id: int
    user: User
    tags: list[Tag] = []

    class Config:
        orm_mode = True