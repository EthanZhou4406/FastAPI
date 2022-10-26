from sqlalchemy import Table,Column,String,Integer,DateTime
from sqlalchemy.orm import mapper

# 相对引入
from ..configs.db import Base

publisher_table = Table(
    "book",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50),comment="出版社名称"),
    Column("address", String(150),comment="出版社地址"),
    comment = "出版社表"
)
# 新的一种混合方式创建数据表模型类
class Publisher(object):
    def __init__(self,**kwargs):
        for i in kwargs:
            self.__dict__[i] = kwargs.get(i)
mapper(Publisher,publisher_table)