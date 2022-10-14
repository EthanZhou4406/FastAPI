
# 导入使用的包

from fastapi import FastAPI  #FastAPI创建FastAPI的一个重要包
import uvicorn   #uvicorn 是异步服务器


# 创建FastAPI实例对象
app = FastAPI()

# get路径装饰器
@app.get("/")
# 路径操作函数，async表示异步操作
async def main():
    return {
        "message":"Helloworld, FastAPI"
    }


#运行服务器
#官方指令：uvicorn No.1_helloworld.py:app  --reload
if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)
