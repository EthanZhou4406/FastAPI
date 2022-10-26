from sqlalchemy.orm import Session
from datetime import datetime
from typing import Union

from models.user import User
from schemas.user import UserIn

def insert_user(db:Session,username:str,hash_pwd:str):
    token = ''
    last_time = datetime.utcnow()
    user = User(username=username,hash_pwd=hash_pwd,token=token,last_time=last_time)
    db.add(user)
    db.commit()
    return True

def update_user(db:Session,id:int,token:Union[str,None]=None,last_time:Union[datetime,None]=None):
    if token:
        db.query(User).filter(User.id == id).update({"token":token})
    if last_time:
        db.query(User).filter(User.id == id).update({"last_time":last_time})
    db.commit()
    return True

def read_user(db:Session, username:str) -> UserIn:
    user = db.query(User).filter(User.username == username).one()
    if user:
        return UserIn(**user.dict())