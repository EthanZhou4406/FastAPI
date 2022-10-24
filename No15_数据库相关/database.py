from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DBURL = 'mysql+pymysql://root:123456@127.0.0.1:3306/dbtest'
engine = create_engine(DBURL)
session = sessionmaker(bind = engine)
Base = declarative_base()