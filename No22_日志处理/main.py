from fastapi import FastAPI,Request
from loguru import logger
from datetime import timedelta

# 第一步：创建一个日志记录器
# 清除默认日志记录器
logger.remove()
# 创建新的日志记录器
# 每天生成一个日志文件，文件名称时年-月-日的形式命名
# 日志文件保存7天
logger.add(
    sink="./No22_日志处理/logs/{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="1 days",
    retention=timedelta(days=7)
    )

app = FastAPI()
@app.on_event("startup")
def startup_event():
    # 在系统启动时，挂载日志记录器
    # 第二步：为app注册一个公共的日志记录器
    app.state.logger = logger

@app.on_event("shutdown")
def shutdown_event():
    # 第四步：清除日志记录器
    app.state.logger.remove()

# 第三步：在路径操作函数中试用日志记录器记录日志
@app.get("/")
# 利用logger.catch装饰器可以记录异常信息
@logger.catch
def getHome(req:Request):
    # 利用req的app属性可以访问到整个app
    req.app.state.logger.info("访问首页")
    return "/home"

if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app='main:app',host="127.0.0.1",port=8080,reload=True)