# 第一步：导入fastapi包
from email.mime import image
from fastapi import FastAPI
# 导入typing包为了提供类型提示的运行时支持
from typing import Union

# 第二步：创建FastAPI类的实例对象

app = FastAPI()

# 演示通过继承BaseModel类来引用请求体参数
# 第三步：创建继承自BaseModel类的子类，用来表示请求体数据模型
# BaseModel子类声明的是一个JSON类型的请求体格式，请求体将当做JSON读取
from pydantic import BaseModel
class Item(BaseModel):
    name:str
    # description 和 tax都是可选字段
    description:Union[str,None] = None  
    price:float
    tax:Union[float,None] = None

# 第四步：创建路径装饰器和路径操作函数
@app.post("/items")
# 在路径操作函数中将形参声明为BaseModel子类的类型
async def create_item(item:Item):
    return item

# 演示Body函数引用数据体参数
from fastapi import Body
@app.put("/items")
# 在路径操作函数中将形参默认值声明为Body函数，表示该形参是请求体中的某个字段
async def update_item(name:str=Body(),tax:float=Body()):
    return {"name":name,"tax":tax}

# 演示dict方式引用请求体参数
from typing import Dict
@app.patch("/items")
# 在路径操作函数中将形参类型设定为Dict类型，表示接收任何符合此类型的键值对作为数据体参数
async def update_part_item(item:Dict[str,str]):
    return item

# 演示对BaseModel方式引入的请求体参数进行限制
# 针对这种类型，首先需要引入Field函数
from pydantic import Field
# 利用Field函数为每个需要做限制的字段设定默认值
class Student(BaseModel):
    name:str = Field(min_length=3)
    age:int = Field(gt=0)
@app.post("/student")
async def create_student(stu:Student):
    return stu

# 演示对Body方式引入的请求体参数进行限制
@app.put("/student")
# 利用Body函数中的参数对每个请求体字段进行限制
async def update_student(name:str=Body(min_length=3),age:int=Body(gt=0)):
    return {"name":name,"age":age}

# 演示嵌套请求体
# 定义一个基础请求体模型
class Image(BaseModel):
    url:str
    name:str
# 定义一个使用了基础请求体模型的嵌套模型
class ImageItem(BaseModel):
    name:str
    description:str
    price:float
    tax:Union[float,None] = None
    image:Union[Image,None] = None

@app.post("/imageitem")
async def create_imageitem(imageItem:ImageItem):
    return imageItem

# 第五步：运行服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app,host="localhost",port=8080)



