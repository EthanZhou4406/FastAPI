'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-10-18 20:37:29
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-10-18 22:17:30
FilePath: No10_请求体更新数据和JSON编码器\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from datetime import datetime
from typing import Union,List

from fastapi import FastAPI,HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


app = FastAPI()

# 演示不使用jsonable_encoder编码
@app.post("/items/{id}")
def insert_item(id: str, item: Item):
    fake_db[id] = item
    print(fake_db) 

# 演示使用jsonable_encoder编码
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    print(fake_db)
""" 不知道为什么返回时两种情况，结果是一致的
# 演示不使用jsonable_encoder编码
@app.post("/item/{id}")
def insert_item(id: str, item: Item):
    fake_db[id] = item
    return fake_db 

# 演示使用jsonable_encoder编码
@app.put("/item/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    return fake_db
 """

#  演示更新数据时默认值产生的后果
class Student(BaseModel):
    name:Union[str,None] = None
    description:Union[str,None] = None
    sex:Union[str,None]=None
    age:int = 18
    hobby:List[str] = []

# 模拟目前存在的一些学生信息
students = [
    {"name":"jack","age":20},
    {"name":"tom","description":"he is a boy","sex":"male"},
    {"name":"jerry","hobby":["basketball","games"]}
]

# 定义路径装饰器和路径操作函数来更新某个student信息
@app.patch("/students/{id}")
async def update_student(id:int,stu:Student):
    if id<len(students):
        students[id]=jsonable_encoder(stu)
    else:
        raise HTTPException(status_code=404,detail="out of range")
    return students

# 演示通过BaseModel子类的dict函数的exclude_unset参数解决此类问题
@app.put("/students/{id}")
async def update_student(id:int,stu:Student):
    if id<len(students):
        # 第一步：取出原存储的数据
        stu_stored = students[id]
        # 第二步：根据原存储数据创建原数据的数据模型对象
        stu_model = Student(**stu_stored)
        # 第三步：利用BaseModel子类的dict函数的exclude_unset参数取出改变的字段字典
        update_data = stu.dict(exclude_unset=True)
        # 第四步：利用BaseModel子类的copy函数的update参数更新指定字段数据
        update_item = stu_model.copy(update=update_data)
        # 第五步：用更新后的数据对象替换原数据对象，完成更换
        students[id]=jsonable_encoder(update_item)
    else:
        raise HTTPException(status_code=404,detail="out of range")
    return students

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app",host="127.0.0.1",port=8080,reload=True)