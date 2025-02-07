from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

app = FastAPI()

MONGO_URI = "mongodb+srv://debruyns:DAMLore@damlore-cluster.qn1o6.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client ["debruyns"]
collection = db["landmarks"]

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
async def get_history(request: Request, tag:str = Query("", alias="tag")):
    available_tags = sorted(set(collection.distinct("tag")))
    if tag: 
        landmarks = list(collection.find({"tag":tag}, {"_id": 0}))
    else:
        landmarks = list(collection.find({},{"_id":0}))
    return templates.TemplateResponse("history.html", {"request": request, "landmarks": landmarks, "available_tags":available_tags, "selected_tag":tag})

@app.get("/tour")
async def get_tour(request: Request):
    return templates.TemplateResponse("tour.html", {"request": request})