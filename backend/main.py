from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api.views import router as api_router

import models
from db import engine

from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from datetime import date, datetime
from fastapi_scheduler import SchedulerAdmin
from fastapi.middleware.cors import CORSMiddleware

from dependency import init_schedule, login_and_reservation
from scheduler import site, scheduler

from fastapi.templating import Jinja2Templates
from fastapi import Request


templates = Jinja2Templates(directory="static")

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(api_router, prefix="/api", tags=["api"])

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})






@app.on_event("startup")
async def startup():
    # Mount the background management system
    site.mount_app(app)
    app.mount("/web", StaticFiles(directory="static"), name="static")

    # Start the scheduled task scheduler
    scheduler.start()

    init_schedule()

