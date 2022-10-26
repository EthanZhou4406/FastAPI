from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session
from schemas.user import UserIn,UserUp
from utils.db import get_db
from utils.token import hash_pwd
from services.user import insert_user,update_user

user = APIRouter()

@user.post("/")
def add_user(user:UserIn,db:Session=Depends(get_db)):
    h_pwd = hash_pwd(user.pwd)
    insert_user(db=db,username=user.username,hash_pwd=h_pwd)
    return {
        "code":"0000",
        "msg":"OK"
    }

@user.put("/")
def modify_user(user:UserUp,db:Session=Depends(get_db)):
    update_user(db=db,token=user.token,last_time=user.last_time,id=user.id)
    return {
        "code": "0000",
        "msg": "OK"
    }

