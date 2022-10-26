from pydantic import BaseModel

class BookIn(BaseModel):
    title:str
    author:int
    publisher:int
    code:str
