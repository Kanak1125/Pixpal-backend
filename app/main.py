import os, shutil
from datetime import datetime
from pathlib import Path

from PIL import Image

from fastapi import FastAPI, Depends, HTTPException, Query, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from typing import Annotated

from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils.populate_db import populate_db

import blurhash

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://127.0.0.1:5500", "http://127.0.0.1:5501"]

SUB_ROOT = "/app"

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

if (len(crud.get_images(skip=0, limit=10, db= get_db())) == 0):
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

@app.get("/tags/", response_model=list[schemas.TagResponse])
def read_tags(db: Session = Depends(get_db)):
    db_tags = crud.get_tags(db = db)
    # return db_tags
    return [tag.list_serialize() for tag in db_tags]

#  response_model= schemas.ImageCreate
@app.post("/images/")
async def create_image(description: str = Form(...), color: str = Form(...), tags: list[str] = Form(...),  uploaded_file: UploadFile = File(...), db: Session = Depends(get_db)):

    directory = Path("seed_images")

    path = directory / uploaded_file.filename

    # print(dir(uploaded_file))

    # img = Image(file.stream)
    # IF NOT img, raise excpeion
    #  img.wdith, img.height
    # IMG.SAVE(path)
    

    # img = Image.open(directory)
    # img = Image.open(uploaded_file.filename)
    # img.save(directory)
    # img.save(f"./app/assets/images/")

    with open(path, "w+b") as fp:
        shutil.copyfileobj(uploaded_file.file, fp)
        shutil.copy2(path, f"./app/assets/images/")

    hash = None

    # with open(path, 'rb') as fp:
    #     hash = blurhash.encode(fp, x_components= 4, y_components= 3)

    with Image.open(path) as image:
        image.thumbnail((100, 100))
        hash = blurhash.encode(image, x_components=4, y_components= 3)

    try:
        img = Image.open(path)
    except Exception as excp:
        return "Not such files allowed other than images..."
    
    img_size = img.size
    width, height = img_size

    image = {
        "blur_hash": hash,
        "created_at": datetime.now(),
        "description": description,
        "alt_description": uploaded_file.filename,
        "width": width,
        "height": height,
        "color": color,
        "file_name": uploaded_file.filename,
        "likes": 0,
    }

    tag_ids = []

    for each in tags:
        db_tag = db.query(models.Tag).filter(models.Tag.title == each).first()
        # print("DB tag ==========>", db_tag)

        if not db_tag:
            new_tag = schemas.Tag(title= each, type= "search")
            newly_created_tag = crud.create_tag(db, tag= new_tag)
            tag_ids.append(newly_created_tag.id)
        else:
            tag_ids.append(db_tag.id)

    pyd_model_images = schemas.ImageCreate(**image, tags=tag_ids)

    return crud.create_image(db, pyd_model_images)

@app.get("/images/", response_model= list[schemas.ImageResponse])
def read_images(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    db_images = crud.get_images(skip= skip, limit= limit, db= db)

    print("DB_IMAGES_DATA ======>", [image.list_serialize() for image in db_images])
    if db_images == None:
        raise HTTPException(status_code=204, detail= "No contents available...")

    return [image.list_serialize() for image in db_images]

@app.get("/image/{image_id}", response_model= schemas.ImageResponse)
def read_image(db: Session = Depends(get_db), image_id: int = 1):
    db_image = crud.get_image(db, image_id)
    # user =
    if db_image == None:
        raise HTTPException(status_code=204, detail= "No contents available...")
    return db_image

@app.get("/search/photos/", response_model= list[schemas.ImageResponse])
def search_images(db: Session = Depends(get_db), q: list[str] | str | None = Query(None), orientation: str | None = None, color: str | None = None, file_type: str | None = None):
    print("\n\n\nQUery ====>", q)
    db_images = crud.get_images_searches(db, q=q, orientation=orientation, color=color, file_type=file_type)

    if q == None or db_images == None:
        raise HTTPException(status_code= 204, detail= "No search results...")

    return [image.list_serialize() for image in db_images]