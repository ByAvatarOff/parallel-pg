from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.transactions.schema.sql_schema import IsolationLevel, PostgresLock


templates = Jinja2Templates(directory="src/templates")

template_router = APIRouter(
    prefix='',
    tags=['app']
)


@template_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "isolations": [isolation for isolation in IsolationLevel],
            "locks": [lock for lock in PostgresLock],
        }
    )
