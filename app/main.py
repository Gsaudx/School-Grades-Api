from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import students
from app.database import load_data, save_data
from app.crud import students_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento ao ligar o servidor
    global students_db
    students_db.update(load_data())
    yield
    # Evento ao desligar o servidor (função para salvar novos estudantes no students.json)
    save_data(students_db)

app = FastAPI(lifespan=lifespan)

app.include_router(students.router)
