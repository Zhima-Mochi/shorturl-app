from pydantic import BaseModel
from fastapi import FastAPI
from typing import List, Optional
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.responses import FileResponse
from utility import *
from sqlalchemy import func
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

HOST_NAME = os.environ['HOST_NAME']
# FRONTEND_HOST_NAME = os.environ['FRONTEND_HOST_NAME']
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[HOST_NAME],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OrigUrl(BaseModel):
    url: str


long_url_code = LongUrlCode()


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    print(request.method)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('./static/favicon.ico')


@app.get("/{code}")
async def redirect_to_original_url(code: str):
    return RedirectResponse(url=long_url_code.decode(code))


@app.post("/")
async def generate_code(given_url_obj: OrigUrl):
    if(not await valid_url(given_url_obj.url)):
        return {'is_success': False}
    print(given_url_obj)
    code = long_url_code.encode(given_url_obj.url)
    return {'is_success': True, 'host_name': HOST_NAME, 'code': code}
