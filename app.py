from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_root(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/map")
async def get_map(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})

@app.get("/about")
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/mission")
async def get_mission(request: Request):
    return templates.TemplateResponse("mission.html", {"request": request})

@app.get("/history")
async def get_history(request:Request):
    return templates.TemplateResponse("history.html", {"request": request})