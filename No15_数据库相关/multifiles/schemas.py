from typing import Union, Union
from pydantic import BaseModel

class ItemBase(BaseModel):
    title:str
    description : Union[str,None] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id : int
    owner_id :int
    # 不声明这个将导致无法获取外键信息
    class Config :
        orm_mode = True

class UserBase(BaseModel):
    email : str

class UserCreate(UserBase):
    password:str

class User(UserBase):
    id : int
    is_active : bool
    items: List[Item] = []

    class Config:
        orm_mode = True