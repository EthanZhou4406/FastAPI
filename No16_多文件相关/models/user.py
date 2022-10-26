from sqlalchemy import Table,Column,String,Integer,DateTime
from sqlalchemy.orm import mapper

# 相对引入
from configs.db import Base


user_table = Table(
    "user",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(20),comment="用户名"),
    Column("hash_pwd", String(200),comment="加密后的密码"),
    Column("token", String(255),comment="token"),
    Column("last_time", DateTime(),comment="最后登录时间"),
    comment = "用户表"
)
# 新的一种混合方式创建数据表模型类
class User(object):
    def __init__(self,**kwargs):
        for i in kwargs:
            self.__dict__[i] = kwargs.get(i)
mapper(User,user_table)
