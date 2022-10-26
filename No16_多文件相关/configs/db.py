from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# 数据库相关的系统配置项
DBURL = 'mysql+pymysql://root:123456@127.0.0.1:3306/libraryDB'
ENGINE = create_engine(DBURL)
Base = declarative_base(bind=ENGINE)
