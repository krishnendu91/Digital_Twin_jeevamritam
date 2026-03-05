from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/img", StaticFiles(directory="img"), name="img")

# simple user system (no database yet)
users = {
    "admin":{"password":"admin123","role":"admin"},
    "researcher":{"password":"research123","role":"researcher"},
    "operator":{"password":"operator123","role":"operator"}
}

# DIGITAL TWIN STATE
digital_twin = {
    "tank1":50,
    "tank2":60,
    "pressure1":1.5,
    "pressure2":1.2,
    "mode":"filter"
}

@app.get("/",response_class=HTMLResponse)
def login_page(request:Request):

    return templates.TemplateResponse("login.html",{"request":request})


@app.post("/login")
async def login(data:dict):

    username = data["username"]
    password = data["password"]

    if username in users and users[username]["password"] == password:
        return {"status":"success"}

    return {"status":"fail"}


@app.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request):

    return templates.TemplateResponse("dashboard.html",{"request":request})


# PHYSICAL LAYER SIMULATION
@app.get("/sensor")
def sensor_data():

    digital_twin["tank1"] = random.randint(30,90)
    digital_twin["tank2"] = random.randint(40,95)

    digital_twin["pressure1"] = round(random.uniform(1.5,2.5),2)
    digital_twin["pressure2"] = round(random.uniform(1.0,2.0),2)

    return digital_twin


# CONTROL API
@app.post("/control")
def control_system(data:dict):

    digital_twin["mode"] = data["mode"]

    print("System mode:", data["mode"])

    return {"status":"ok","mode":data["mode"]}