from fastapi import FastAPI
import uvicorn

from untils.register import register_app
from routers.router import root


app = FastAPI(title="一个完整的项目系统演示")
register_app(app=app)
app.include_router(router=root)


if __name__ == "__main__":
    uvicorn.run(app="main:app",host="127.0.0.1",port=9090,reload=True)