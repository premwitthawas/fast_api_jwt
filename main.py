from fastapi import FastAPI
from utils.tages import Tages

from routes.auth_route import router as auth_router

app = FastAPI()


# HEALTH CHECK
@app.get("/", tags=[Tages.HEALTCHECK])
async def get_healtcheck():
    return {"mesasge": "API IS WORKING! "}


app.include_router(auth_router,prefix="/api/v1/auth",tags=[Tages.AUTH])
