import os
import logging
from datetime import datetime

from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


# 配置项常量
STATIC_PATH = "./No21_时间处理器_startup&shutdown/static"
UPLOAD_PATH = "./No21_时间处理器_startup&shutdown/upload"
LOG_PATH = "./No21_时间处理器_startup&shutdown/logs"
LOGGER = logging.getLogger()

# 文件挂载
def file_handler(app:FastAPI):
    if not os.path.exists(STATIC_PATH):
        os.mkdir(STATIC_PATH)

    if not os.path.exists(UPLOAD_PATH):
        os.mkdir(UPLOAD_PATH)

    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    app.mount('/static',StaticFiles(directory=STATIC_PATH),name="static")



# 中间件
def middle_handler(app:FastAPI):
    # 跨域共享middleware
    allow_origin = ["*"]
    app.add_middleware(CORSMiddleware,allow_origin=allow_origin)

    # 自定义记录处理时长中间件
    @app.middleware("http")
    async def process_time_middleware(req:Request,call_next):
        start = datetime.now()
        resp = await call_next(req)
        end = datetime.now()
        resp.headers['X-process-time']=str(end-start)
        return resp

# 数据库
def db_handler(app:FastAPI):
    @app.on_event("startup")
    def get_redis():
        


app = FastAPI()
file_handler(app=app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host="127.0.0.1", port=8080, reload=True , debug=True)

