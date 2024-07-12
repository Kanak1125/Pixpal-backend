import os
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import crud, models
from .database import engine
from .utils.populate_db import populate_db

from .routers import images, tags
from .utils.db_session import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

SUB_ROOT = "/app"

app.add_middleware(
    CORSMiddleware,
    allow_origins= json.loads(os.getenv("ORIGINS")),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# populate the db if there is no image data...
if (len(crud.get_images(skip=0, limit=10, db= get_db())) == 0):
    db = get_db()
    populate_db(db)
else:
    print("There is already data in the table...")

app.include_router(images.router)
app.include_router(tags.router)

# Determine the absolute path for the images directory
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
images_directory = os.path.join(current_directory, './assets/images')

# Check if the images directory exists
if not os.path.isdir(images_directory):
    raise RuntimeError(f"Directory '{images_directory}' does not exist")

app.mount("/images", StaticFiles(directory=images_directory), name="images")