from app.database import *

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()