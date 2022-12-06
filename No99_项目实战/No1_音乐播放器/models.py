from sqlalchemy import Table,Column,create_engine,String,Time,Integer
from sqlalchemy.orm import Session,registry

mapper_registry = registry()
metadata = mapper_registry.metadata
Base = mapper_registry.generate_base()


music_table = Table(
    "musicPlayer_musics",
    metadata,
    Column("id",Integer,primary_key=True,autoincrement=True,comment='主键id'),
    Column("singer",String(20),comment='歌手'),
    Column("name",String(20),comment="歌名"),
    Column("time",Time,comment='时长'),
    Column("path",String(255),comment="存储路径"),
    comment="音乐表"
)

class Music(Base):
    __table__ = music_table


if __name__ == "__main__":
    metadata.create_all(create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/projects'))