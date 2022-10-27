'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-10-27 21:41:58
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-10-27 22:08:49
FilePath: No17_后台应用\multibackgroundtask.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import Union
import time

from fastapi import BackgroundTasks,Depends,FastAPI

app = FastAPI()

# 定义一个后台应用函数
def write_log(message:str):
    with open("log1.txt",mode="a") as log:
        log.write(message+'\n')

# 定义一个嵌套的后台应用函数
def get_query(background_tasks:BackgroundTasks,q:Union[str,None] = None):
    if q:
        message = f"found query: {q}"
        background_tasks.add_task(write_log,message)
    print("依赖函数执行完毕")
    return q

@app.post("/send-notification/{email}")
async def send_notification(
    email:str, background_tasks:BackgroundTasks,q:str = Depends(get_query)
):
    message = f"message to {email}"
    background_tasks.add_task(write_log,message)
    print("路径操作函数执行完毕")
    time.sleep(5)
    return {"message":"message sent","q":q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("multibackgroundtask:app",host="127.0.0.1",port=8080,reload=True)