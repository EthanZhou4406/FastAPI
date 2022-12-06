from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from crud import *
from untils import *


musicPlayer = FastAPI()
musicPlayer.add_middleware(CORSMiddleware,allow_origins=['*'])

@musicPlayer.get("/musics")
def query_musics(db:Session=Depends(get_db)):
    data = get_musics(db=db)
    if len(data)>0:
        return {
            "code":"0000",
            "msg":"查询成功",
            "data":data,
            "count":len(data)
        }
    else:
        return {
            "code":"0000",
            "msg":"查询无记录"
        }

if __name__ == '__main__':
    uvicorn.run(app='main:musicPlayer',host="127.0.0.1",port=8080,reload=True)