'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-10-16 19:44:40
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-10-16 21:59:15
FilePath: No8_响应状态码和处理错误\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 第一步：导入FastAPI类
from signal import raise_signal
from fastapi import FastAPI
# 第二步：创建FastAPI示例对象
app = FastAPI()
# 第三步：创建路径修饰器
# 演示默认响应状态码
@app.get("/item")
# 第四步：创建路径操作函数
async def get_item():
    return {"msg":"请求成功"}

# 演示将成功响应时状态码改为其它
# 演示通过数字方式修改状态码
from fastapi import Body
@app.post("/item",status_code=201)
async def create_item(user=Body(),pwd=Body()):
    users = []
    users.append({"username":user,"pwd":pwd})
    return {
        "result":"create successfully"
    }

# 演示通过枚举方式修改状态码
# 从fastapi包中引入status，用来修改成功响应时状态码
from fastapi import status
# 此处虽然使用了400状态码，但是浏览器依旧能够得到结果。说明此处的状态码只要路径操作函数成功执行完都会得到此处的状态码
@app.patch("/item",status_code=status.HTTP_400_BAD_REQUEST)
async def update_item(name:str=Body(),price:float=Body()):
    return {
        "result":"查无结果"
    }

# 演示通过HTTPException来修改错误发生时状态码
# 从fastapi中引入HTTPException类表示异常
from fastapi import HTTPException
@app.get("/items/{item_id}")
async def get_items(item_id:int=0):
    if item_id == 3:
        # status_code表示响应码，detail表示发生异常时响应的JSON格式内容
        # 异常响应式也可以添加响应头内容
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Don't have this item_id ",
        headers={"X-token":"test"})
    else:
        return {
            "item_id":item_id
        }

# 演示自定义异常处理器过程
# 第一步：自定义异常类
class MyException(Exception):
    def __init__(self, name: str) -> None:
        self.name = name

# 第二步：添加自定义异常控制器
# 导入Request是表示HTTP请求的类
# 导入JSONResponse是表示HTTP是JSON格式响应
# 导入这两个类用于添加自定义异常控制器
from fastapi import Request
from fastapi.responses import JSONResponse
# 创建一个异常处理器
@app.exception_handler(MyException)
# 创建异常处理器操作函数，此处形参一个为请求，另一个为自定义异常类！
# 异常处理器操作函数体中声明，状态码，响应信息和其他处理逻辑
async def myexception_handler(req:Request,exc:MyException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "message":f"{exc.name} is not allowed"
        }
    )

# 第三步：使用自定义异常处理器
from fastapi import Query
@app.get("/student/")
async def get_stu(name:str=Query()):
    if name == "test":
        raise MyException(name=name)
    else:
        return {
            "name":name
        }

# 演示覆盖默认异常处理器，主要使用是重新定义异常处理器操作函数
# 演示覆盖HTTPException JSON格式回复给文本回复
# 引入fastapi中的PlainTextResponse是为了修改异常回复格式为文本
from fastapi.responses import PlainTextResponse
@app.exception_handler(HTTPException)
async def http_exception_handler(req,exc):
    return PlainTextResponse(
        status_code=exc.status_code,
        content=str(exc.detail)
    )

@app.get("/student/{stu_id}")
async def get_stu(stu_id:int = 0):
    if stu_id == 3:
        raise HTTPException(status_code=418,detail="Not 3")
    return {"stu_id":stu_id}

# 第五步：运行服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app",host="127.0.0.1",port=8080,reload=True)