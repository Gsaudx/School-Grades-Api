from fastapi import FastAPI
from app.routers import students
from app.database import load_data, save_data
from app.crud import students_db

app = FastAPI()

#On server/api start
@app.on_event("startup")
def startup_event():
    global students_db
    students_db.update(load_data())

#on server/api shut down
@app.on_event("shutdown")
def shutdown_event():
    save_data(students_db)

app.include_router(students.router)
