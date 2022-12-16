from pydantic import BaseSettings

class Settings(BaseSettings):
    '''
    Settings类用来获取系统的配置信息。
    其主要包括数据库连接的相关配置信息
    '''
    mysql_db : str
    redis_host : str
    redis_pwd : str
    redis_port : int
    redis_db : int

    class Config:
        env_file = "./No24_项目架构/configs/.env"
