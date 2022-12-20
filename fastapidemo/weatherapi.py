from fastapi import FastAPI,Path,Request
from fastapi import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel


weatherlist = [
  {
    "date": "2022-12-15",
    "temperatureC": 30,
    "temperatureF": 85,
    "summary": "Chilly"
  },
  {
    "date": "2022-12-16",
    "temperatureC": 51,
    "temperatureF": 123,
    "summary": "Bracing"
  },
  {
    "date": "2022-12-17",
    "temperatureC": -9,
    "temperatureF": 16,
    "summary": "Cool"
  },
  {
    "date": "2022-12-18",
    "temperatureC": -7,
    "temperatureF": 20,
    "summary": "Bracing"
  },
  {
    "date": "2022-12-19",
    "temperatureC": -18,
    "temperatureF": 0,
    "summary": "Bracing"
  }
]

app = FastAPI()


@app.get("/forecast")
def weather():
    return weatherlist

@app.get("/forecast/{id}")
def weatherbyid(id: int = Path(None, description="Get forecast by id")):
    return weatherlist[id]

@app.post("/forecast")
async def newforecast(weather: Request):

    return await weather.json()