'''
Author: Ethan.Zhou ethanzhou4406@outlook.com
Date: 2022-11-05 07:15:24
LastEditors: Ethan.Zhou ethanzhou4406@outlook.com
LastEditTime: 2022-11-05 16:21:04
FilePath: No20_安全性_高级版\oath2.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# oauth2 区域认证用来给用户或app特定的权限。
# oauth2中的区域可以理解为string类型的列表，且列表中每个string不能包含空格

from datetime import datetime,timedelta
from typing import List,Union

from fastapi import Depends,FastAPI,HTTPException,Security,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm,SecurityScopes

from jose import JWSError,jwt
from passlib.context import CryptContext
from pydantic import BaseModel,ValidationError


#用于加密的密钥和算法及用户token过期时间
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 模拟数据库中存储的用户数据
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}

# 创建token返回数据模型
class Token(BaseModel):
    access_token:str
    token_type:str

# 创建token解析数据模型
class TokenData(BaseModel):
    username:Union[str,None] = None
    scopes:List[str] = []

# 创建用户数据模型
class User(BaseModel):
    username:str
    email:Union[str,None] = None
    full_name:Union[str,None] = None
    disabled:Union[bool,None] = None

class UserInDB(User):
    hashed_password:str

# 定义加密模式
pwd_context = CryptContext(schemes=["bcrypt"],deprecated='auto')

# 定义登录地址及用户权限。
# 此处设定scopes主要作用是用在docs中显示可选的几个scope，实际开发中可以不添加
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "me":"Read information about the current user",
        'items':'Read items'
    }
)

app = FastAPI()

# 验证密码是否正确
def verify_password(plain_pwd,hashed_pwd):
    return pwd_context.verify(plain_pwd,hashed_pwd)

# 生成加密的密码
def get_hashed_password(password):
    return pwd_context.hash(password)

# 根据用户名在数据库中获取用户信息
def get_user(db,username:str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# 用户登录认证，验证用户名是否存在，密码是否正确
def authenticate_user(db,username:str,password:str):
    user = get_user(db=db,username=username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user

# 创建token信息
def create_access_token(data:dict,expires:Union[timedelta,None]=None):
    to_encode = data.copy()
    if expires:
        expire = datetime.now() + expires
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    #生成jwt token
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

# 解析token，获取用户相关信息（user,scopes等，根据定义来获得)
# security_scopes表示被访问的路径所需的权限
async def get_current_user(
    security_scopes:SecurityScopes,token:str=Depends(oauth2_scheme)
):
    # 获取scopes
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    # 定义认证失败的报错
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate":authenticate_value}
    )
    try:
        # jwt解密token
        playload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        # 获取token中的用户名信息，sub是根据后面的/token路径操作函数中定义得来
        username = playload.get("sub")
        if username is None:
            raise credentials_exception
        # 获取token中的scopes信息，scopes是根据后面的/token路径操作函数中定义得来
        token_scopes = playload.get("scopes",[])
        token_data = TokenData(username=username,scopes=token_scopes)
    except(JWSError,ValidationError):
        raise credentials_exception
    user = get_user(db=fake_users_db,username=token_data.username)
    if user is None:
        raise credentials_exception
    # 检查该路径访问所需的权限名称，在该用户token包含的scopes中是否都具有，否则报错
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate":authenticate_value}
            )
    return user

# 定义获取当前激活用户的依赖函数
async def get_current_active_user(
    # Security是Depends的子类，用来表示该路径所需的权限名称
    current_user:User = Security(get_current_user,scopes=['me'])
):
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user

# 定义登录接口,返回用户的token
@app.post("/token",response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends()):
    user = authenticate_user(fake_users_db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=400,detail="Incorrent username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.username,"scopes":form_data.scopes},
        expires=access_token_expires
    )
    return {"access_token":access_token,"token_type":"bearer"}

# 定义需要me权限的访问路径
@app.get("/users/me",response_model=User)
async def read_users_me(current_user:User=Depends(get_current_active_user)):
    return current_user

# 定义需要me和items权限的访问路径
@app.get("/users/me/items/")
async def read_own_items(
    current_user: User = Security(get_current_active_user, scopes=["items"])
):
    return [{"item_id": "Foo", "owner": current_user.username}]

# 定义需要用户登录的访问路径
@app.get("/status/")
async def read_system_status(current_user: User = Depends(get_current_user)):
    return {"status": "ok"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='oath2:app',host='127.0.0.1',port=8080,reload=True)