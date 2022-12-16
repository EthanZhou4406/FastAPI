from fastapi.routing import APIRouter

test = APIRouter()

@test.get("/")
async def get_test():
    return {
        "code":"00000"
    }