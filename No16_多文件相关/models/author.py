from sqlalchemy import Table,Column,String,Integer,DateTime
from sqlalchemy.orm import mapper

# 相对引入
from ..configs.db import Base

author_table = Table(
    "book",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50),comment="作者姓名"),
    comment= "作者表"
)
# 新的一种混合方式创建数据表模型类
class Author(object):
    def __init__(self,**kwargs):
        for i in kwargs:
            self.__dict__[i] = kwargs.get(i)
mapper(Author,author_table)
