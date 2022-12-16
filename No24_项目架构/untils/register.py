'''
记录系统启动时注册的日志，用户验证等信息
'''
import sys
import traceback
from datetime import timedelta
from time import time
from loguru import logger
from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException,RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from untils.codes import RespCode


def init_logger():
    '''
    创建一个日志记录器：
    支持两种显示方式，终端显示，文件存储（保存周期7天)
    '''
    # 清除系统默认日志记录方式
    logger.remove()
    # 添加终端显示日志记录方式
    logger.add(sink=sys.stderr,format="{time:YYYY/MM/DD HH:mm:ss} | {level} | {message}")
    # 添加文件记录日志方式
    logger.add(
        sink="./No24_项目架构/logs/{time:YYYYMMDD}.log",
        format="{time:YYYY/MM/DD HH:mm:ss} | {level} | {message}",
        rotation="1 days",
        retention=timedelta(days=7))
    return logger



def register_app(app:FastAPI) -> None:
    '''
    注册app各个环节内容，包括启动时挂载日志系统，中间件处理，异常处理
    '''
    @app.on_event("startup")
    async def start_app():
        # 挂载日志系统
        app.state.logger = init_logger()

    # 数据类型验证异常处理
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request,exc):
        app.state.logger.error(f'参数错误|{request.url}|{request.headers}|{str(exc.errors())}')
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({
                "code":RespCode.INVALID_DATA.code,
                "msg":"参数不全或参数错误",
                "data":{
                    "tip":exc.errors(),
                    "body":exc.body
                }
            })
        )
    
    # 断言类型验证异常处理
    

    # 异常处理
    @app.exception_handler(Exception)
    async def http_exception_handler(request,exc):
        app.state.logger.error(f"全局错误|{request.url}|{request.headers}|{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code":RespCode.SYSTEM_ERROR.code,
                "msg":"服务器错误"
            }
        )
    # 添加跨域请求中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    # 添加服务器处理时间中间件
    @app.middleware("http")
    async def add_process_time(req:Request,call_next):
        start = time()
        client_host = req.client.host
        client_port = req.client.port
        request_method = req.method
        resp = await call_next(req)
        end = time()
        req.app.state.logger.info(f'{client_host}:{client_port} | {request_method} | {(end-start)*1000} ms | {resp.status_code}')
        return resp

    # 添加用户权限认证
    @app.middleware("http")
    async def check_auth(req:Request,call_next):
        path = req.url.path
        print(path)
        resp = await call_next(req)
        return resp

    

    @app.on_event("shutdown")
    async def close_app():
        pass
        # 关闭redis数据库
