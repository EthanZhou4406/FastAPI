from email.policy import default
from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index = True)
    email = Column(String(50),unique=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean,default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(50))
    description = Column(String(255))
    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("User",back_populates="items")

