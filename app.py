from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse

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


@app.get("/", tags=["Root"], response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content="""
    <html>
        <head>
            <title>Welcome to AidAgent API</title>
        </head>
        <body>
            <h1>Welcome to AidAgent API</h1>
            <p>Visit our <a href="/docs">API documentation</a> to explore the available endpoints.</p>
        </body>
    </html>
    """)


from fastapi import FastAPI
from routes.user import router as user_router
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(alert_router, prefix="/alerts", tags=["Alerts"])
app.include_router(charity_router, prefix="/charities", tags=["Charities"])
app.include_router(donation_router, prefix="/donations", tags=["Donations"])
app.include_router(form_router, prefix="/forms", tags=["Forms"])