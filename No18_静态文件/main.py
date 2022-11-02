'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-10-29 06:32:18
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-11-02 20:21:14
FilePath: No18_静态文件\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import sys

app = FastAPI()

# mount表示在应用中绑定了独立的子应用，且子应用的访问路径以/static开头
# 该子应用详细的实现是StaticFiles
# 该子应用的访问别名是static，该别名通常使用在前端中
app.mount("/static",StaticFiles(directory="No18_静态文件/static"),name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app',host='127.0.0.1',port=8080,reload=True)