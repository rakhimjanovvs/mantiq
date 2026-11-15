from fastapi import FastAPI

from app import models
from app.routers import courses, lessons


app = FastAPI(title="Mantiq")
app.include_router(courses.router)
app.include_router(lessons.router)
