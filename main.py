from fastapi import FastAPI
from db.database import engine
from db import models
from routers import employees


app = FastAPI()

app.include_router(employees.router)

models.Base.metadata.create_all(bind=engine)
