import os
from urllib.parse import urlparse

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, FileSystemLoader

from src.analyze import analyze


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def middleware(request: Request, call_next):
    if request.method == "HEAD":
        response = Response()
    elif "herokuapp" in urlparse(str(request.url)).netloc:
        domain = os.getenv("DOMAIN")
        if domain:
            url = urlparse(str(request.url))._replace(netloc=domain).geturl()
            response = RedirectResponse(url)
        else:
            response = await call_next(request)
    else:
        response = await call_next(request)
    return response


@app.get("/")
async def read_root():
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(__file__), encoding="utf8")
    )
    html = env.get_template("index.html").render()
    return HTMLResponse(content=html, status_code=200)


@app.get("/analyze")
async def get_analyze(text: str):
    return analyze(text)
