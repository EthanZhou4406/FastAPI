'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-10-17 20:34:10
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-10-17 22:08:13
FilePath: No9_响应模型\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 演示在fastapi中如何使用响应模型
# 第一步：引入fastapi中FastAPI类，用于创建应用实例对象
from lib2to3.pytree import Base
from string import hexdigits
from unicodedata import name
from fastapi import FastAPI

# 第二步：创建FastAPI类的实例对象
app = FastAPI(title="演示响应模型的API")

# 第三步：导入pydantic中BaseModel类用于创建数据模型
# EmailStr一个满足email格式的字符串
from pydantic import BaseModel,EmailStr

# 第四步：创建数据模型
# InUser类用来表示用户输入数据模型
class InUser(BaseModel):
    name:str
    pwd:str
    email:EmailStr

# DBUser类用来表示数据在数据库中的数据模型
class DBUser(BaseModel):
    name:str
    hash_pwd:str
    email:EmailStr

# OutUser类用来表示输出数据模型(响应模型)
class OutUser(BaseModel):
    name:str
    email:EmailStr

# 导入hashlib用于进行md5加密pwd
import hashlib
# 定义hash_pwd模型加密密码
def hash_pwd(pwd:str):
    h1 = hashlib.md5()
    h1.update(pwd.encode(encoding='utf-8'))
    return h1.hexdigest()

# 定义save_user用来模拟将数据存储到数据库中
def save_user(user:InUser):
    pwd = hash_pwd(user.pwd)
    # user.dict()表示数据模型的dict方式
    # **表示将dict表示成key=value,...方式
    dbuser = DBUser(**user.dict(),hash_pwd=pwd)
    print("user create in db") 
    return dbuser

# 第五步：创建路径装饰器和路径操作函数，
# 并在路径装饰器中使用response_model指定相应模型
@app.post("/user",response_model=OutUser)
async def create_user(user:InUser):
    dbuser = save_user(user=user)
    return dbuser

# 演示路径修饰器中响应模型相关参数的使用
from typing import Union
class Item(BaseModel):
    name:str
    description : Union[str,None] = None
    price:float = 1.0

# 演示不使用响应模型相关参数的返回结果
@app.post("/item",response_model=Item)
async def create_item(item:Item):
    return item

# 演示使用response_model_exclude_unset参数
@app.patch("/item",response_model=Item,response_model_exclude_unset=True)
async def update_item(item:Item):
    return item

# 演示使用response_model_include参数
@app.delete("/item",response_model=Item,response_model_include={"name","price"})
async def delete_item(item:Item):
    return item

# 第六步：运行服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app",host="127.0.0.1",port=8080,reload=True)
