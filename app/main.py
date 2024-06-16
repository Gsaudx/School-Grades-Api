from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import students
from app.database import load_data, save_data
from app.crud import students_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    global students_db
    students_db.update(load_data())
    yield
    # Shutdown event
    save_data(students_db)

app = FastAPI(lifespan = lifespan)

app.include_router(students.router)
