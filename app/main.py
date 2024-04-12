from PIL import Image

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils.populate_db import populate_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://127.0.0.1:5500", "http://127.0.0.1:5501"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: 
        return db
    finally: 
        db.close()

if (len(crud.get_images(get_db())) == 0):
    db = get_db()
    populate_db(db)
else:
    print("There is already data in the table...")

# @app.get("/")
# def say_something():
#     return {"msg": "Something here"}

@app.post("/tags/", response_model= schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db, id = tag.id)
    if db_tag:
        raise HTTPException(status_code= 400, detail= "Tag already exists...")
    return crud.create_tag(db= db, tag= tag)

@app.get("/tags/", response_model=list[schemas.Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = crud.get_tags(db = db, skip= skip, limit= limit)
    return tags

@app.post("/images/", response_model= schemas.Image)
def create_image(image: schemas.ImageCreate, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, id = image.id)
    if db_image:
        raise HTTPException(status_code= 400, detail= "Image already exits...")
    return crud.create_image(db= db, image= image)

@app.get("/images/", response_model= list[schemas.ImageResponse])
def read_images(db: Session = Depends(get_db)):
    db_images = crud.get_images(db)

    print("DB_IMAGES_DATA ======>", [image.list_serialize() for image in db_images])
    if db_images == None:
        raise HTTPException(status_code=204, detail= "No contents available...")
    # return {
    #     **db_images,
    # }
    return [image.list_serialize() for image in db_images]

@app.get("/image/{image_id}", response_model= schemas.ImageResponse)
def read_image(db: Session = Depends(get_db), image_id: int = 1):
    db_image = crud.get_image(db, image_id)
    # user = 
    if db_image == None:
        raise HTTPException(status_code=204, detail= "No contents available...")
    return db_image