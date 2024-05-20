import requests
import time
from pathlib import Path

from fastapi import FastAPI

app = FastAPI()

BASE_URL = 'https://api.unsplash.com/'

UNSPLASH_CLIENT_ID = "U-JKAdSdHZRA2-glU6Oe4WSzqHGP6GpKM8DZ8yUkelY&query"

IMAGE_FILE = 'images/download.jpg'
DOWNLOAD_DIRNAME = "seed_images"
BASE_PARAMS = {
    "key": UNSPLASH_CLIENT_ID,
    "type": "photos"
}

response = requests.get(f"{BASE_URL}{BASE_PARAMS['type']}/?client_id={UNSPLASH_CLIENT_ID}")

results = enumerate(response.json())
print("Results", results)

for idx, each in results:
    # directory = os.path.dirname(IMAGE_FILE)

    resp = requests.get(each['urls']['regular'])
    directory = Path(DOWNLOAD_DIRNAME)
    if not directory.exists():
        directory.mkdir()

    path = directory / f"image-{idx}.jpg"

    with open(path, "wb") as fp:
        fp.write(resp.content)

    time.sleep(0.1)


@app.get('/')
async def get_res():
    return {"results", results}