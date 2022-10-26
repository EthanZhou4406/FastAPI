from sqlalchemy import Table,Column,String,Integer,DateTime
from sqlalchemy.orm import mapper

# 相对引入
from configs.db import Base

book_table = Table(
    "book",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(50),comment="书名"),
    Column("author", Integer,comment="作者，作者表的id"),
    Column("publisher", Integer, comment="出版社，出版社表的id"),
    Column("code", String(20), comment="ISBN码"),
    comment = "图书表"
)
# 新的一种混合方式创建数据表模型类
class Book(object):
    def __init__(self,**kwargs):
        for i in kwargs:
            self.__dict__[i] = kwargs.get(i)
mapper(Book,book_table)