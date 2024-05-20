from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal
from app.utils.db_session import get_db

router = APIRouter()

router = APIRouter(
    prefix="/api"
)

@router.post(f"/tags/", response_model= schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db, id = tag.id)
    if db_tag:
        raise HTTPException(status_code= 400, detail= "Tag already exists...")
    return crud.create_tag(db= db, tag= tag)

@router.get(f"/tags/", response_model=list[schemas.TagResponse])
def read_tags(db: Session = Depends(get_db)):
    db_tags = crud.get_tags(db = db)
    # return db_tags
    return [tag.list_serialize() for tag in db_tags]