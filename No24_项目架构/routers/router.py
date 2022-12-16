from fastapi.routing import APIRouter
from views.test import test

root = APIRouter(prefix="/api/v1")
root.include_router(router=test)