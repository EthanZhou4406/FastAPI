'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-10-14 22:34:45
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-10-15 21:19:17
FilePath: No7_相应模型\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import imp
from importlib.metadata import files
from random import paretovariate
from fastapi import FastAPI


# 演示获取表单数据的步骤
# 第一步：导入Form函数
from fastapi import Form

# 第二步：创建一个FastAPI类的实例对象
app = FastAPI()

# 第三步：创建一个路径装饰器
@app.post("/register")
# 第四步：创建一个路径操作函数，声明Form表单变量
async def create_user(username: str = Form(), password: str = Form()):
    return {
        "result": "register successfully",
        "username": username,
        "password": password
    }

# 演示接收文件数据
# File方式,利用File来声明这个变量接收的是一个文件数据
from fastapi import File
@app.post("/file/file")
# 此处的...表示None，...表示省略第一个形参
# filename需要和前端的变量名一致
async def get_file(filename:bytes = File(...)):
    return {"file_size":len(filename)}

# 演示UploadFile类接收文件数据
# UploadFile方式，利用UploadFile来声明变量的类型
from fastapi import UploadFile
@app.post("/file/uploadfile")
async def get_uploadfile(file:UploadFile):
    # UploadFile 的属性如下：
    # filename：上传文件名字符串（str），例如， myimage.jpg；
    # content_type：内容类型（MIME 类型 / 媒体类型）字符串（str），例如，image/jpeg；
    # file： SpooledTemporaryFile（ file-like 对象）。其实就是 Python文件，可直接传递给其他预期 file-like 对象的函数或支持库。
    # UploadFile 支持以下 async 方法，（使用内部 SpooledTemporaryFile）可调用相应的文件方法。
    # write(data)：把 data （str 或 bytes）写入文件；
    # read(size)：按指定数量的字节或字符（size (int)）读取文件内容；
    # seek(offset)：移动至文件 offset （int）字节处的位置；
    # 例如，await myfile.seek(0) 移动到文件开头；
    # 执行 await myfile.read() 后，需再次读取已读取内容时，这种方法特别好用；
    # close()：关闭文件。
    # 因为上述方法都是 async 方法，要搭配「await」使用。
    # 例如，在 async 路径操作函数 内，要用以下方式读取文件内容：
    # contents = await myfile.read()
    # 在普通 def 路径操作函数 内，则可以直接访问 UploadFile.file，例如：
    # contents = myfile.file.read()
    return{
        "filename":file.filename,
        "content_type":file.content_type
    }

# 演示File和UploadFile接收多文件数据
# 接收多文件时需要将接收文件类型的参数，声明为包含文件的列表形式
from typing import List
@app.post("/files/file")
async def get_files(files:List[bytes]=File(...)):
    return {
        "file_number":len(files)
    }
    
@app.post("/files/uploadfile")
async def get_files(files:List[UploadFile]):
    filesname = [file.filename for file in files]
    return { "filesname":filesname}

# 演示既接收Form数据又接收文件数据
@app.post("/mixdata")
async def get_mixdata(username=Form(),file:UploadFile=File()):
    return {
        "username":username,
        "filename":file.filename
    }



# 第五步：运行服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8080, reload=True)
