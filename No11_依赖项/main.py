'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-10-19 20:25:15
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-10-19 22:03:47
FilePath:No11_依赖项\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import Union

from fastapi import Depends,Cookie,FastAPI,Header,HTTPException
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# 步骤1：创建依赖函数，和定义函数没有区别
async def common_parameters(
    q:Union[str,None] = None,
    skip:int = 0,
    limit:int = 100
):
    return {
        "q":q,
        "skip":skip,
        "limit":limit
    }

# 步骤2：在路径操作函数中使用依赖函数
# 要使用依赖项，需要引入fastapi中的Depends函数
@app.get("/items")
async def read_items(commons:dict = Depends(common_parameters)):
    return commons

@app.get("/users")
async def read_users(commons:dict = Depends(common_parameters)):
    return commons

# 步骤1：创建公共类
class CommonQueryParams:
    def __init__(self,q:Union[str,None]=None,skip:int = 0,limit:int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

# 步骤2：在路径操作函数中引入公共类
@app.get("/item")
# 引入依赖类的简写方式为：common：CommonQueryParams=Depends()
async def read_item(common:CommonQueryParams=Depends(CommonQueryParams)):
    return jsonable_encoder(common)

# 下面演示嵌套依赖

# 定义最外层依赖函数
def query_extractor(q:Union[str,None] = None):
    print("q")
    return q

# 定义依赖最外层依赖函数的依赖函数
def query_or_cookie_extractor(
    q:str=Depends(query_extractor),
    last_query:Union[str,None]=Cookie(default=None)
    ):
    print("cookie")
    if not q:
        return last_query
    return q

# 定义使用了嵌套依赖函数的路径操作函数
@app.post("/items")
# use_cache表示是否针对多次使用同一个依赖项使用缓存
def create_items(query_or_default:str = Depends(query_or_cookie_extractor,use_cache=False)):
    return {"q_or_cookie":query_or_default}

# 演示路径中添加无返回值的依赖项
async def verify_token(x_token:str=Header()):
    if not x_token:
        raise HTTPException(status_code=400,detail="not X-Token header invalid")

async def verify_key(x_key:str=Header()):
    if not x_key:
        raise HTTPException(status_code=400,detail="not X-Key header invalid")

@app.get("/student",dependencies=[Depends(verify_key),Depends(verify_token)])
async def read_student():
    return {"msg":"hello"}
    
# 演示创建全局依赖，被某个应用中的所有路径依赖
app1 = FastAPI(dependencies=[Depends(verify_key),Depends(verify_token)])
@app1.get("/student")
async def read_student():
    return {"msg":"hello"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app",host="127.0.0.1",port=8080,reload=True)