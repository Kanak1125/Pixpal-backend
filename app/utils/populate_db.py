import os, time, shutil
from pathlib import Path

import requests

from sqlalchemy.engine import reflection
from app.models import Image
from app.database import Base, engine

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

def populate_db(db):
    print("The length of the images in table in db is 0...")

    response = requests.get(f"{BASE_URL}{BASE_PARAMS['type']}/?client_id={UNSPLASH_CLIENT_ID}")

    results = enumerate(response.json())
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

    for idx, each in results:
        directory = os.path.dirname(IMAGE_FILE)
        print(directory)

        resp = requests.get(each['urls']['regular'])

        directory = Path(DOWNLOAD_DIRNAME)
        if not directory.exists():
            directory.mkdir()

        path = directory / f"image-{idx}.jpg"

        with open(path, "wb") as fp:
            fp.write(resp.content)
            shutil.copy2(path, f"./app/assets/images/")

        if (idx == 0):
            pyd_model_users = schemas.UserCreate(**user)
            crud.create_user(db, pyd_model_users)

        pyd_model_images = schemas.ImageBase(file_name=f"image-{idx}.jpg" ,**each)

        crud.create_image(db, pyd_model_images)
        
        
        time.sleep(0.1)