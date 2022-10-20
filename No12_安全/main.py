from fastapi import FastAPI,Depends,HTTPException,status
# OAuth2PasswordBearer用来指定生成token的路径
# OAuth2PasswordRequestForm用来指定生成token操作函数的输入
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union

# fake_users_db用来模拟数据库中存储的用户信息
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

# 用户数据模型
class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

# 用户在数据库中的数据模型
class UserInDB(User):
    hashed_password: str

# 用来加密密码
def fake_hash_password(password: str):
    return "fakehashed" + password

app = FastAPI()

# 第一步：指定创建token的路径，通常和登录为同一个路径
# OAuth2PasswordBearer被调用时会去获取header中是否有Authorization的值
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# 第二步：创建token路径的路径装饰器和路径操作函数
@app.post("/login")
# 在创建token中以OAuth2PasswordRequestForm为依赖，作为请求体
# OAuth2PasswordRequestForm默认接收username和password的form数据
async def login(form_data:OAuth2PasswordRequestForm=Depends()):
    # 根据用户名首先判断该用户名在数据库中是否存在，如果不存就报错
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400,detail="Incorrect username")
    # 然后获取该用户名在数据库中的加密后的密码
    user = UserInDB(**user_dict)
    # 根据后端固定的加密规则对输入的用户密码进行加密，
    # 然后对比本次输入的加密密码和数据库中存储的加密密码是否一致，不一致报错
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400,detail="Incorrect pwd")
    # 用户名和密码都验证通过后，生成token返回前端
    # 通常有一个方法来生成token，此处为了简单，直接用username作为token返回前端
    # token_type指定token的类型，是OAuth2协议的规定
    return {
        "access_token":user.username,
        "token_type":"bearer"
    }

# 第三步：在后面的请求中，首先都要进行安全性验证
# 即通过token来验证用户信息

# 定义根据用户名在数据库中获取用户信息
def get_user(db,username:str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# 定义解密token的方法
def fake_decode_token(token):
    user = get_user(fake_users_db,token)
    return user

# 定义获取当前用户的方法
# 依赖oauth2_scheme去获取请求头中是否有Authorization，其对应的值应该是token
async def get_current_user(token:str = Depends(oauth2_scheme)):
    # 解析token
    user = fake_decode_token(token)
    # 用户不存在时报错
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            # 此处的headers回复时OAuth2的规定
            headers={"WWW-Authenticate": "Bearer"}
            )
    return user

# 模拟再次请求
@app.get("/users/me")
# 依赖验证token的方法进行二次请求，满足验证时响应，否则报错
async def read_users_me(current_user:User=Depends(get_current_user)):
    return current_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app",host="127.0.0.1",port=8080,reload=True)



