from fastapi import FastAPI, Depends

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.alert import router as alert_router
from routes.charity import router as charity_router
from routes.user import router as user_router
from routes.donation import router as donation_router
from routes.form import router as form_router
app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


from fastapi import FastAPI
from routes.user import router as user_router
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(alert_router, prefix="/alerts", tags=["Alerts"])
app.include_router(charity_router, prefix="/charities", tags=["Charities"])
app.include_router(donation_router, prefix="/donations", tags=["Donations"])
app.include_router(form_router, prefix="/forms", tags=["Forms"])