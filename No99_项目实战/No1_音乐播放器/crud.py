from sqlalchemy.orm import Session
from models import *

def get_musics(db:Session):
    records = db.query(Music).all()
    data = []
    for record in records:
        data.append({
            "id":record.id,
            "singer":record.singer,
            "name":record.name,
            "time":record.time,
            "path":record.path
        })
    return data