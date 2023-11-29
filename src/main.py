import uvicorn
from fastapi import FastAPI

from src.user.router import user_router
from src.auth.router import auth_router

app = FastAPI()


app.include_router(user_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=1488, reload=True)

