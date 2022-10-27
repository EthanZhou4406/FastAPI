'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-10-27 21:12:02
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-10-27 21:36:26
FilePath: No17_后台应用\singlebackgroundtask.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 导入包
from fastapi import FastAPI,BackgroundTasks
from datetime import datetime



app = FastAPI()

# 定义后台运行函数
def send_email(email:str,message:str):
    with open("log.txt",mode='a+') as email_file:
        content = f"notification for {email}: {message}"
        email_file.writelines(content)

@app.post("/send-notification/{email}")
#在路径操作函数中添加BackgroundTasks类的参数
async def send_notification(email:str, bt:BackgroundTasks):
    # 将后台运行函数，添加到BackgroundTasks实例对象中，并传入后台运行函数的形参值
    bt.add_task(send_email,email,message=datetime.now().isoformat())
    return {"message":"Notification sent in the background"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("singlebackgroundtask:app",host="127.0.0.1",port=8080,reload=True)
