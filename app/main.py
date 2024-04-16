from PIL import Image

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils.populate_db import populate_db

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
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_tags = crud.get_tags(db = db, skip= skip, limit= limit)
    # return db_tags
    return [tag.list_serialize() for tag in db_tags]

@app.post("/images/", response_model= schemas.Image)
def create_image(image: schemas.ImageCreate, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, id = image.id)
    if db_image:
        raise HTTPException(status_code= 400, detail= "Image already exits...")
    return crud.create_image(db= db, image= image)

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
def search_images(db: Session = Depends(get_db), q: list[str] | str | None = Query(None)):
    print("\n\n\nQUery ====>", q)
    db_images = crud.get_images_searches(db, q)
    
    if q == None or db_images == None:
        raise HTTPException(status_code= 204, detail= "No search results...")
    
    return [image.list_serialize() for image in db_images]