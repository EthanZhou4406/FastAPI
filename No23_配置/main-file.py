'''
在之前的项目中，代码中都暴露了一些隐私的信息，例如连接数据库等连接信息。
本节就是讲解在fastapi中如何不暴露这些信息
'''
'''
方法2：
将隐私内容存放在本地配置文件中，通过读取配置文件获取隐私配置文件
'''
from functools import lru_cache
from pydantic import BaseSettings
from fastapi import FastAPI,Depends

class Settings(BaseSettings):
    # 类似BaseModel一样，配置各个配置项的内容限制和数据类型
    dburl:str

    class Config:
        # env_file配置配置文件的路径
        env_file = "./No23_配置/config/.env"
app = FastAPI()

@lru_cache
def get_settings():
    # 缓存配置项设置
    return Settings()

@app.get("/")
def get_home(settings:Settings=Depends(get_settings)):
    return {
        "db_url":settings.dburl
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main-file:app",host="127.0.0.1",port=8080,reload=True)
    