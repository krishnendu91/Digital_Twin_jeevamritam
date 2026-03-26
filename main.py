from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import uvicorn

app = FastAPI()

# 🔹 ThingSpeak Config
WRITE_API_KEY = "XOUX7OHDJ0IENP6A"
READ_API_KEY = "TUZL9B4DT35EXA7G"
CHANNEL_ID = "3311967"

# 🔹 Templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/img", StaticFiles(directory="img"), name="img")

# 🔹 Users
users = {
    "admin":{"password":"admin123","role":"admin"},
    "researcher":{"password":"research123","role":"researcher"},
    "operator":{"password":"operator123","role":"operator"}
}

# ================= LOGIN =================
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(data: dict):

    if data["username"] in users and users[data["username"]]["password"] == data["password"]:
        return {"status": "success"}

    return {"status": "fail"}


# ================= DASHBOARD =================
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# ================= READ FROM THINGSPEAK =================
@app.get("/thingspeak")
def read_thingspeak():

    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}"

    try:
        res = requests.get(url, timeout=5)
        data = res.json()

        return {
            "tank1": int(data.get("field2") or 50),
            "tank2": int(data.get("field3") or 60),
            "pressure1": float(data.get("field4") or 1.5),
            "pressure2": float(data.get("field5") or 1.2),
            "mode": int(data.get("field1") or 0)
        }

    except:
        return {
            "tank1": 50,
            "tank2": 60,
            "pressure1": 1.5,
            "pressure2": 1.2,
            "mode": 0
        }


# ================= WRITE TO THINGSPEAK =================
@app.post("/control")
def control(data: dict):

    mode = data["mode"]

    if mode == "filter":
        value = 1
    elif mode == "backwash":
        value = 2
    else:
        value = 0

    try:
        requests.get(
            "https://api.thingspeak.com/update",
            params={
                "api_key": WRITE_API_KEY,
                "field1": value
            },
            timeout=5
        )
    except:
        pass

    return {"status": "ok", "mode": mode}


# ================= RUN =================
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)