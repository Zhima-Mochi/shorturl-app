from typing import List
from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import aiohttp
import crud
import models
import schemas
from database import SessionLocal, engine
import os


HOST_NAME = os.environ['HOST_NAME']
# FRONTEND_HOST_NAME = os.environ['FRONTEND_HOST_NAME']

models.Base.metadata.create_all(bind=engine)

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

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def valid_url(url):
    try:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.get(url) as resp:
                return resp.status == 200
    except:
        return False


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    print(request.method)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('./static/favicon.ico')


@app.get("/{code}")
async def redirect_to_original_url(code: str, db: Session = Depends(get_db)):
    return RedirectResponse(url=crud.get_longUrl(db, code))


@app.post("/")
async def generate_code(given_url_obj: schemas.OrigUrl, db: Session = Depends(get_db)):
    if(not await valid_url(given_url_obj.url)):
        return {'is_success': False, 'message': '這是一個無效的網址'}
    print(given_url_obj)
    code_elem = crud.get_code(db, given_url_obj.url)
    if not code_elem:
        code_elem = crud.create_code(db, given_url_obj.url)
    if code_elem['status']:
        return {'is_success': True, 'host_name': HOST_NAME, 'code': code_elem['code']}
    else:
        return {'is_success': False, 'message': '內部錯誤'}
