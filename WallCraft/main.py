from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from . import user_router, admin_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.include_router(user_router.router)
app.include_router(admin_router.router)
