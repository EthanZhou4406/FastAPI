from typing import Union

from fastapi import  FastAPI

app = FastAPI()

# 声明一个用户类的请求体类型
from pydantic import BaseModel
class User(BaseModel):
    userName:str
    pwd:str

# 演示服务端向客户端发送cookie信息
# 导入fastapi中的Response类用来设置cookie
from fastapi import Response
@app.post("/register/")
def createUser(user:User,response:Response):
    response.set_cookie(key="userName",value=user.userName)
    response.set_cookie(key="pwd",value=user.pwd)
    return {"result":"register successfully"}

# 演示服务端从客户端读取cookie信息
# 导入fastapi中的Cookie函数用来表示cookie
from fastapi import Cookie
@app.get("/items/{item_id}")
# 此处需要注意cookie定义的名称需要和客户端中cookie的key的名称一致！！！
def get_items(item_id:int,userName:Union[str,None]=Cookie(default=None),pwd:Union[str,None]=Cookie(default=None)):
    return {
        "item_id":item_id,
        "userName":userName,
        "pwd":pwd
    }

# 演示获取请求头的相关信息
# 导入fastapi中的Header函数用来表示header
from fastapi import Header
@app.get("/demo")
# 由于正常请求头中key的命名是这样的User-Agent，如何以这个作为变量名python认为是非法的变量命名
# 由于这种冲突fastapi中会将user_agent当做User-Agent。
# 如果不想使用这种默认的解决冲突方式需要，在Header函数中使用convert_underscores=False
def demo(user_agent:Union[str,None]=Header(None,convert_underscores=True),postman_token:Union[str,None]=Header(None)):
    return{
        "User-Agent":user_agent,
        "Postman-Token":postman_token
    }

# 演示获取一个请求头具有多个值的情况
# 要获取多个值的请求头信息，需要将对应的请求头变量的类型设置为列表类型
from typing import List
@app.get("/demos")
def demos(x_token:Union[List[str],None]=Header(default=None,convert_underscores=True)):
    return {
        "X-Token":x_token
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app",host="localhost",port=8080,reload=True)
