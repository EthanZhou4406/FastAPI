'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-10-26 20:05:07
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-10-26 20:07:46
FilePath: No16_多文件相关\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI
from routers.user import user
from routers.book import book

from configs.db import Base

app = FastAPI()
@app.on_event("startup")
def initdb():
    Base.metadata.create_all()


app.include_router(user,prefix="/user",tags=["用户相关"])
app.include_router(book,prefix="/book",tags=["图书相关"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app",host="127.0.0.1",port=8080,reload=True)