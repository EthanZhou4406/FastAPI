'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-11-02 20:21:40
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-11-05 07:15:03
FilePath: No19_依赖_中间件_后台应用\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI,BackgroundTasks,Depends,Request

# 创建一个FastAPI实例对象
app = FastAPI(title="演示依赖——中间件——后台应用的执行顺序")

# 创建一个依赖函数
async def dependfun():
    print("来自依赖函数的输出")
    return None

# 创建一个中间件
@app.middleware("http")
async def middlewarefun(req:Request,call_next):
    print("来自中间件请求部分的输出")
    resp = await call_next(req)
    print("来自中间件响应部分的输出")
    return resp

# 创建一个后台应用函数
async def backgroundfun():
    print("来自后台函数的输出")

# 创建一个路径修饰器及其路径操作函数
@app.get("/")
async def test(bt:BackgroundTasks,md=Depends(dependfun)):
    bt.add_task(backgroundfun)
    print("来自路径操作函数的输出")
    return {"msg":"OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app",host="127.0.0.1",port=8080)