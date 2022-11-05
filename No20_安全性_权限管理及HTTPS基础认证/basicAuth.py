'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-11-05 11:00:31
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-11-05 17:14:13
FilePath: No20_安全性_权限管理及HTTPS基础认证\basicAuth.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 导入secrets用于进行字符串比较
import secrets

from fastapi import Depends,FastAPI,HTTPException,status
from fastapi.security import HTTPBasic,HTTPBasicCredentials

app = FastAPI()

# 创建HTTPBasic实例对象，作为依赖项，实现弹窗效果
security = HTTPBasic()
# HTTPBasicCredentials是HTTPBasic()返回类型，包含录入的username和password信息
def get_current_username(credentials:HTTPBasicCredentials=Depends(security)):
    # 对获取的username和password进行utf8编码
    current_username_bytes = credentials.username.encode("utf8")
    username_in_db_bytes = b"fakeuser"
    # 防止黑客攻击，利用secrets的compare_digest方法比较录入值和正确值是否一致
    is_correct_username = secrets.compare_digest(username_in_db_bytes,current_username_bytes)
    if is_correct_username:
        current_pwd_bytes = credentials.password.encode("utf8")
        pwd_in_db_bytes = b"fakepwd"
        is_corrent_pwd = secrets.compare_digest(pwd_in_db_bytes,current_pwd_bytes)
        if is_corrent_pwd:
            return credentials.username
        else:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrent username or pwd",
            headers={"WWW-Authenticate":"Basic"}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrent username or pwd",
            headers={"WWW-Authenticate":"Basic"}
        )

@app.get("/users/me")
def read_current_user(username:str=Depends(get_current_username)):
    return {
        "username":username
    }

@app.get("/item/{item_id}")
def get_item(item_id:int):
    return{
        "item_id":item_id
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='basicAuth:app',host='127.0.0.1',port=8080,reload=True)