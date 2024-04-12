import os, time, shutil
from pathlib import Path
import json
import requests

from sqlalchemy.engine import reflection
from app.models import Image, Tag, User
from app.database import Base, engine, SessionLocal

from app import crud, schemas


BASE_URL = 'https://api.unsplash.com/'

UNSPLASH_CLIENT_ID = "U-JKAdSdHZRA2-glU6Oe4WSzqHGP6GpKM8DZ8yUkelY&query"

IMAGE_FILE = 'local_images/download.jpg'
DOWNLOAD_DIRNAME = "seed_images"

BASE_PARAMS = {
    "key": UNSPLASH_CLIENT_ID,
    "type": "photos"
}

insp = reflection.Inspector.from_engine(engine)

tags = ['space', 'animal', 'sky', 'blue', 'night', 
        'mars', 'alien', 'travel', 'mountain', 'beach']




def populate_db(db):
    print("The length of the images in table in db is 0...")

    # response = requests.get(f"{BASE_URL}{BASE_PARAMS['type']}/?client_id={UNSPLASH_CLIENT_ID}")
    # r_text = response.content.decode("utf-8", "replace")

    # print(r_text[274:291])
    # with open(Path("app") / "assets" / "fixtures.json", "wb") as f:
    #     f.write(response.content)

    with open(Path("app") / "assets" / "fixtures.json", "rb") as f:
        results = json.load(f)
    
    # results = enumerate([1, 2, 3, 4, 5])

    # DUMMY USER...
    user = {
        'first_name': "Alien",
        'last_name': "Helion",
        'username': "alienHelion",
        'profile_image_url': "http://something.com/image.jpg",
        'email': "alien@gmail.com",
        'password': "alien123"
    }


    user_obj = db.query(User).filter(User.email == user["email"]).first()
    if user_obj is None:
        user_pyd_obj = schemas.UserCreate(**user)
        user_obj = crud.create_user(db, user_pyd_obj)


    tag1 = db.query(Tag).filter(Tag.title == "water").first()
    if tag1 is None:
        tag1 = Tag(id=202, title="water", type="search")
    
    tag2 = db.query(Tag).filter(Tag.title == "old").first()
    if tag2 is None:
        tag2 = Tag(id=304, title="old", type="search")

    db.add_all((tag1, tag2))
    db.commit()

    for idx, each in enumerate(results):
        directory = os.path.dirname(IMAGE_FILE)
        print(directory)

        resp = requests.get(each['urls']['regular'])

        directory = Path(DOWNLOAD_DIRNAME)
        if not directory.exists():
            directory.mkdir()

        path = directory / f"image_{idx}.jpg"

        with open(path, "wb") as fp:
            fp.write(resp.content)
            shutil.copy2(path, f"./app/assets/images/")


        # image1 = Image(id= 101, blur_hash='skdjf3jj33r3', created_at="some data", description= "lskjdfklj", alt_description= "ksjdfk", width=234, height= 800, color= "#ff0023", likes= 123, file_name="abc.jpg", tags=[tag1, tag2])

        # db.add_all([tag1, tag2, image1])
        # db.commit()

        # pyd_model_images = schemas.ImageBase(file_name=f"image_{idx}.jpg", **each)
        py_model_tags = schemas.TagBase(title= tags[idx], type= "search")
        crud.create_tag(db, py_model_tags)

        pyd_model_images = schemas.ImageCreate(file_name=f"image_{idx}.jpg",**each, tags=[202, 304])


        crud.create_image(db, pyd_model_images)
        
        time.sleep(0.1)

    image = db.query(Image).get(1)
    tag = db.query(Tag).get(1)
    print("IMage --->", image, "Tag ---->", tag)