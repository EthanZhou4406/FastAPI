from jose import JWTError,jwt
from typing import Union
from datetime import timedelta,datetime

from configs.token import CONTEXT,SECRET_KEY,ALGORITHM

def hash_pwd(pwd:str) -> str:
    return CONTEXT.hash(pwd)

def verify_pwd(p_pwd:str,h_pwd:str) -> bool:
    return CONTEXT.verify(p_pwd,h_pwd)

def create_token(data:dict,expires_delta:Union[timedelta,None]=None) -> str:
    to_encode = data.copy()
    # 追加过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # 注意此处的to_encode中的键，解token后也通过这些键来取值！
    # 利用密钥和加密算法生成token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

