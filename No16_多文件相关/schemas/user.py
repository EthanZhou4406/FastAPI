from pydantic import BaseModel
from typing import Union
from datetime import datetime

class UserIn(BaseModel):
    username:str
    pwd:str
class UserUp(BaseModel):
    id:int
    token:Union[str,None]=None
    last_time:Union[datetime,None]=None