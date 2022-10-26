from sqlalchemy.orm import Session

from configs.db import ENGINE

def get_db():
    db = Session(ENGINE)
    try:
        yield  db
    finally:
        db.close()