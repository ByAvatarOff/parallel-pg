from fastapi import FastAPI
from src.transactions.routers.router import app_router
from src.transactions.routers.tempate_router import template_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(app_router)
app.include_router(template_router)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

