from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

DBURL = "mysql+pymysql://root:123456@127.0.0.1:3306/testdb"
ENGINE = create_engine(DBURL)
SESSION = Session(ENGINE)
BASE = declarative_base()

from sqlalchemy import Column,Integer,String,Float,Boolean,ForeignKey
from sqlalchemy.orm import relationship
class User(BASE):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, autoincrement=True)
	email = Column(String(200),unique=True)
	hashed_password = Column(String(200))
	is_active = Column(Boolean, default=True)
	items = relationship("Item", back_populates="owner")

class Item(BASE):
	__tablename__ = "items"
	id = Column(Integer,primary_key=True,autoincrement=True)
	title = Column(String(20))
	description = Column(String(255))
	owner_id = Column(Integer,ForeignKey("users.id"))
	owner = relationship("User",back_populates="items")

from typing import List,Union
from pydantic import BaseModel
class ItemBase(BaseModel):
	title:str
	description:Union[str,None] = None
class ItemCreate(ItemBase):
	pass
class ItemIn(ItemBase):
	id:int
	owner_id:int
	class Config:
		orm_mode = True
class UserBase(BaseModel):
	email:str
class UserCreate(UserBase):
	password:str
class UserIn(UserBase):
	id:int
	is_active:bool
	items:List[ItemIn] = []
	class Config:
	# orm_mode即可以以data['id']又可以以data.id方式获取数据
		orm_mode = True

def get_user(db:Session,user_id:int):
	return db.query(User).filter(User.id == user_id).first()
def get_user_by_email(db:Session,email:str):
	return db.query(User).filter(User.email == email).first()
def get_users(db:Session,skip:int =0,limit:int=100):
	return db.query(User).offset(skip).limit(limit).all()
def create_user(db:Session,user:UserCreate):
	faked_hashed_password = user.password + "notreallyhashed"
	db_user = User(email=user.email,hashed_password=faked_hashed_password)
	db.add(db_user)
	db.commit()
	# 将数据库自定义的列添加到db_user中，如id
	db.refresh(db_user)
	return db_user

def get_items(db:Session,skip:int=0,limit:int=100):
	return db.query(Item).offset(skip).limit(limit).all()
def create_user_item(db:Session,item:ItemCreate,user_id:int):
	db_item = Item(**item.dict(),owner_id=user_id)
	db.add(db_item)
	db.commit()
	db.refresh(db_item)
	return db_item

from typing import List
from fastapi import Depends,FastAPI,HTTPException
# 创建所有数据表
BASE.metadata.create_all(ENGINE)

app = FastAPI()
# 定义依赖项
def get_db():
	db = Session(ENGINE)
	try:
		yield db
	finally:
		db.close()
		
@app.post("/users/", response_model=UserIn)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@app.get("/users/", response_model=List[UserIn])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=UserIn)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model=ItemIn)
def create_item_for_user(
    user_id: int, item: ItemCreate, db: Session = Depends(get_db)
):
    return create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=List[ItemIn])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    return items

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app,host="127.0.0.1",port=8080)