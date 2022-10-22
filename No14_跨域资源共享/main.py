from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins
)
@app.get("/student")
async def read_student(student_id=Query()):
    return {"student_id":student_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app',host="127.0.0.1",port=8001,reload=True)