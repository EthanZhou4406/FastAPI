from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def get_db() -> Session:
    db_url='mysql+pymysql://root:123456@127.0.0.1:3306/projects'
    engine = create_engine(url=db_url)
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


