import json
from mimetypes import MimeTypes

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.dialects import postgresql

from . import models, schemas

mime = MimeTypes()

# def make_url(mime_type, bin_data):
#     return 'data:'+f_mime+';base64, '+bin_data

## Singleton pattern

def get_image(db: Session, image_id: int):
    result = db.query(models.Image).filter(models.Image.id == image_id).first()
    # response = {
    #     json.dumps(result)
    # }
    return result

def get_images(db: Session):
    # return db.query(models.Image).options(joinedload(models.Image.user_id)).all()
    # query = (db.query(models.Image)).compile(dialect=postgresql.dialect, compile_kwargs={"literal_binds": True})

    print("QUERY ----->", db.query(models.Image))

    return db.query(models.Image).all()

def create_image(db: Session, image: schemas.ImageCreate):
    # instance of models.Image...

    # url = 
    db_image = models.Image(blur_hash= image.blur_hash, created_at= image.created_at, description= image.description, alt_description= image.alt_description, width= image.width, height = image.height, color = image.color, likes = image.likes, file_name= image.file_name, user_id= 1)

    # tags and url to be included....
    
    # response = {
    #     "id": db_image.id,
    #     "blur_hash": db_image.blur_hash,
    #     "created_at": db_image.created_at,
    #     "description": db_image.description,
    #     "alt_description": db_image.alt_description,
    #     "width": db_image.width,
    #     "height": db_image.height,
    #     "color": db_image.color,
    #     "likes": db_image.likes,
    #     "user": {
    #         "id": db_image.user.id,
    #         "username": db_image.user.username,
    #         "email": db_image.user.email,
    #     }
    # }

    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(title=tag.title, type=tag.type)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(first_name=user.first_name, last_name= user.last_name, username= user.username, profile_image_url= user.profile_image_url, email= user.email, password= user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user