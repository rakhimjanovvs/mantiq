from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import courses, lessons

Base.metadata.create_all(engine)

app = FastAPI(title="Mantiq")
app.include_router(courses.router)
app.include_router(lessons.router)
