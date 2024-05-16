import os, shutil
from datetime import datetime
from pathlib import Path

import colorsys

from PIL import Image

from fastapi import Depends, HTTPException, Query, Form, File, UploadFile, APIRouter
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import SessionLocal
from ..utils.db_session import get_db

import blurhash

router = APIRouter(
    prefix="/api"
)

BASE_ROUTE = "api"

@router.post(f"/images/")
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
    number_of_decimals = 4

    colorDict = eval(color)  # convert str to dict...
    hsvColor = colorsys.rgb_to_hsv(round(colorDict["r"] / float(256), number_of_decimals), round(colorDict["g"] / float(256), number_of_decimals), round(colorDict["b"] / float(256), number_of_decimals))

    image = {
        "blur_hash": hash,
        "created_at": datetime.now(),
        "description": description,
        "alt_description": uploaded_file.filename,
        "width": width,
        "height": height,
        "color": "{0}".format(hsvColor),
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

@router.get(f"/images/", response_model= list[schemas.ImageResponse])
def read_images(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    db_images = crud.get_images(skip= skip, limit= limit, db= db)

    print("DB_IMAGES_DATA ======>", [image.list_serialize() for image in db_images])
    if db_images == None:
        raise HTTPException(status_code=204, detail= "No contents available...")

    return [image.list_serialize() for image in db_images]

@router.get("image/{0}".format("{image_id}"), response_model= schemas.ImageResponse)
def read_image(db: Session = Depends(get_db), image_id: int = 1):
    db_image = crud.get_image(db, image_id)
    # user =
    if db_image == None:
        raise HTTPException(status_code=204, detail= "No contents available...")
    return db_image

@router.get(f"/search/photos/", response_model= list[schemas.ImageResponse])
def search_images(db: Session = Depends(get_db), q: list[str] | str | None = Query(None), orientation: str | None = None, color: str | None = None, file_type: str | None = None):
    print("\n\n\nQUery ====>", q)
    db_images = crud.get_images_searches(db, q=q, orientation=orientation, color=color, file_type=file_type)

    if q == None or db_images == None:
        raise HTTPException(status_code= 204, detail= "No search results...")

    return [image.list_serialize() for image in db_images]