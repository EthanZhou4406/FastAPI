'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-10-21 21:14:07
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-10-21 22:02:55
FilePath: No13_中间件\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI,status,Request,Response

import time
app = FastAPI()

# 中间件是各个路径操作函数共同拥有的逻辑处理函数
# 利用fastapi的middleware("http")装饰器表名下面的函数是一个中间件
# 表名该app下的路径操作函数都会受该中间件影响
@app.middleware("http")
# 中间件函数的形参必须有两个：
# 第一个为Request的实例对象，
# 第二个表示一个回调函数，并以Request实例对象作为输入
# 返回值必须为call_next的结果，或加工后的结果
async def process_timer(req:Request,call_next):
    # 响应部分
    start_time = time.time()
    print("上方请求处理")
    # call_next的调用表明其下方是响应部分
    response = await call_next(req)
    process_time = time.time() - start_time
    response.headers["X-process-Time"] = str(process_time)
    print("上方响应处理")
    return response

@app.middleware("http")
async def process_token(req:Request,call_next):
    token = req.headers.get("X-token")
    if not token:
        return Response(content="token not available",status_code=status.HTTP_401_UNAUTHORIZED)
    print("下方请求处理")
    res = await call_next(req)
    print("下方响应处理")
    return res



@app.get("/item/{item_id}")
async def read_item(item_id:int):
    return {"item_id":item_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app",host="127.0.0.1",port=8080,reload=True)
