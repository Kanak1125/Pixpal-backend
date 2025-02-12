# Pixpal (Image Discovery Site)

Pixpal is an image discovery site that allows users to search for images by keyword. The site uses the API built using the fastAPI in the backend to fetch images based on the user's search query. Users can also view the images, get the related images and download them.

The backend of the project is built with the FastAPI framework as it is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

## Features
Some features of this site includes:

- Search for images by keyword
- Filter images by:
    - Image Orientation
    - Image File Type
    - Image color (Average color of the image)
- Infinite scrolling

## Installation
To run this project, you need to have Python 3.6+, and pip installed on your machine. You can install the required packages by running the following command:

```bash
pip install -r requirements. txt
```

Similarly, to start the server change the directory to the app directory and run the following command:

```bash
uvicorn main:app --reload
```

or,

from the root directory you can run the following command:

```bash
uvicorn app.main:app --reload
```

And, [here](https://github.com/Kanak1125/Pixpal-frontend) is the link to the frontend repo of this project.

And Wait a moment, Don't forget to add this in your env file:

```bash
DB_HOST=<your_db_host>
DB_NAME=<your_db_name>
DB_USER=<your_db_user>
DB_PASS=<your_db_pass>
ORIGINS=<your_frontend_url>
```