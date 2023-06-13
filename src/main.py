from fastapi import FastAPI
from user_prefence import get_recommendations_tf

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "server is runnnnnnnig"}

@app.get("/user")
async def user_prefence(activity: str ="Outdoor" ,category: str = "Beach", latitude: float = -1.212555 , longitude : float=116.98106 ):
    data = get_recommendations_tf(activity, category, latitude, longitude)
    return {"preferences": data}
