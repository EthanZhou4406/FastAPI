'''
用来演示获取用户输入参数的各种情况
'''
# 第一步：导入FastAPI包
from fastapi import FastAPI

# 第二步：创建FastAPI类的实例对象
app = FastAPI()


# 演示无类型路径参数
# 第三步：创建路径装饰器
@app.get("/item/{item_id}")

# 第四步：定义路径操作函数
async def getItem(item_id):
    return {
        "item_id":item_id
    }



# 演示有类型路径参数
@app.get("/items/{page_num}")
async def getItems(page_num:int):
    return{
        "current_page":page_num,
        "items":[1,2,3]
    }

# 演示有限制路径参数
# fastapi中通过Path函数来对路径参数进行限制
from fastapi import Path
@app.get("/item/large/{item_id}")
async def getLargeItem(item_id:int = Path(gt=100)):
    return {"largeItem":item_id}

# 演示正则限制的路径参数
# fastapi中通过Path函数中的regex参数进行正则规则验证限制
@app.get("/test/{regex_path}")
async def getRegexPath(regex_path:str = Path(regex="^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$")):
    return {"right_path":regex_path}

# 演示必填查询参数
# fastapi中当遇到操作路径函数中存在非路径参数的形参时，会将其解释为查询参数
students = [
    {"id":"001","name":"Jack","age":19},
    {"id":"002","name":"Rose","age":18},
    {"id":"003","name":"Tom","age":21},
    {"id":"004","name":"Jarry","age":20},
]
@app.get("/student")
async def getStu(name:str,age:int):
    stus = []
    for stu in students:
        # 此处不可以stu.name和stu.age出现否则会报错，和形参名称相同导致
        if stu["name"] == name and stu["age"] >= age:
            stus.append(stu)
    return {"students":stus}

# 演示可选查询参数
# fastapi中当查询参数具有默认值的时候，该查询参数就是可选查询参数
# 导入Union类，是为了表示复合类的数据类型
from typing import Union
@app.get("/students")
# Python中语法规则要求可选查询参数必须要在必填查询参数后面出现
async def getStus(age:int,name:Union[str,None]=None):
    stus = []
    for stu in students:
        if name:
            if stu['name'] == name and stu['age'] > age:
                stus.append(stu)
        else:
            if stu['age'] > age:
                stus.append(stu)
    return {"students":stus}

# 演示有限制查询参数
# 在fastapi中当想对查询参数进行限制的时候，需要导入Query方法
from fastapi import Query
@app.get("/limit/stus")
async def getStuByName(name:Union[str,None] = Query(default=None,min_length=4)):
    for stu in students:
        if stu['name'] == name:
            return {"student":stu}

# 演示请求体参数
# 在fastapi中通过Pydantic来声明请求体
# 第一步：导入pydantic包中的BaseModel类
from pydantic import BaseModel

# 第二步：自定义一个继承自BaseModel的类作为请求体的数据模型
class Student(BaseModel):
    id:str
    name:str
    age:int

@app.post('/student')
# 第三步：将自定义的数据模型类作为形参的数据类型
async def addStu(info:Student):
    students.append(info)
    return {"students":students}


# 演示多参数类型同时出现的场景
class Item(BaseModel):
    name:str
    description:Union[str,None] = None
    price: float
    tax:Union[float,None] = None

@app.put("/items/{item_id}")
# item_id为路径参数
# item为请求体参数
# q为查询参数
async def create_item(item_id:int,item:Item,q:Union[str,None] = None):
    # item.dict()将请求体转化为字典
    # **将字典进行解引用，指向每个key的真实value
    result = {"item_id":item_id, **item.dict()}
    if q:
        result.update({"q":q})
    return result



# 第五步：运行服务器
if __name__ == "__main__":
    import uvicorn
    # 利用uvicorn包的run方法直接运行服务器
        # app指定FastAPI类的实例对象
        # host指定服务器ip
        # port指定端口
    uvicorn.run(app=app,host="localhost",port=8080)
