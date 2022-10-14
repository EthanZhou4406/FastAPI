# 第一步：导入fastapi包
from email.mime import image
from fastapi import FastAPI
# 导入typing包为了提供类型提示的运行时支持
from typing import Union

# 第二步：创建FastAPI类的实例对象
# 演示修改信息区的内容
app = FastAPI(title="引用请求体参数API",
            version="1.0.0",
            description="这里描述了引用请求体参数的三种方式的API",
            openapi_url="/api/api.json",
            docs_url="/swageui",
            redoc_url="/redocui")

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
# 演示通过修改请求方法的形参修改交互文档显示的内容
@app.post("/items",tags=["BaseModel"],summary="通过继承BaseModel引用请求体数据",description="这是一个描述")
# 在路径操作函数中将形参声明为BaseModel子类的类型
async def create_item(item:Item):
    '''
    ## 创建一个货物
    - item表示一个获取的相关信息
    '''
    return item

# 演示Body函数引用数据体参数
from fastapi import Body
@app.put("/items",tags=["BaseModel"],summary="通过Body函数引用请求体数据")
# 在路径操作函数中将形参默认值声明为Body函数，表示该形参是请求体中的某个字段
async def update_item(name:str=Body(),tax:float=Body()):
    return {"name":name,"tax":tax}

# 演示接口界面信息修改
from fastapi import Query
@app.get("/items",description="这个是一个查询参数引用的示例API",summary="查询一个商品")
async def read_items(
    q:Union[str,None] = Query(default=None,
    title="Query String",
    min_length=3,
    description="Query string for the items to search in the database that have a good match",
    example="query",
    deprecated=True)
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# 第五步：运行服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app,host="localhost",port=8080)



