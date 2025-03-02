from fastapi import FastAPI, Form, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from fastapi.responses import JSONResponse

app = FastAPI()

MONGO_URI = "mongodb+srv://debruyns:DAMLore@damlore-cluster.qn1o6.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["debruyns"]
collection = db["landmarks"]

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/map")
async def get_map(request: Request):
    # Fetch landmarks from MongoDB
    landmarks = list(collection.find({}, {"_id": 0, "name": 1, "location": 1, "description": 1}))

    # Format the landmarks as markers
    markers = []
    for landmark in landmarks:
        location = landmark["location"].split(",")
        if len(location) == 2:
            lat, lng = float(location[0]), float(location[1])
            markers.append({
                "lat": lat,
                "lng": lng,
                "info": f"<b>{landmark['name']}</b><br>{landmark['description']}"
            })

    # Pass markers to the template
    return templates.TemplateResponse("map.html", {"request": request, "markers": markers})

@app.get("/about")
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/mission")
async def get_mission(request: Request):
    return templates.TemplateResponse("mission.html", {"request": request})

@app.get("/history")
async def get_history(request: Request, tag: str = Query("", alias="tag")):
    available_tags = sorted(set(collection.distinct("tag")))
    if tag:
        landmarks = list(collection.find({"tag": tag}, {"_id": 0}))
    else:
        landmarks = list(collection.find({}, {"_id": 0}))
    return templates.TemplateResponse("history.html", {"request": request, "landmarks": landmarks, "available_tags": available_tags, "selected_tag": tag})

@app.get("/tour")
async def get_tour(request: Request):
    return templates.TemplateResponse("tour.html", {"request": request})

@app.get("/adder")
async def get_adder(request: Request):
    return templates.TemplateResponse("adder.html", {"request": request})

@app.post("/adder")
async def post_adder(
    name: str = Form(...),
    image_url: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    location_name: str = Form(...),
    id_tag: str = Form(None),
):
    new_landmark = {
        "name": name,
        "image_url": image_url,
        "description": description,
        "location": location,
        "location_name": location_name,
        "tag": id_tag
    }
    collection.insert_one(new_landmark)
    return {"message": "Landmark added successfully!"}
