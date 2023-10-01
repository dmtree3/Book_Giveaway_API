from fastapi import FastAPI
from .database import engine
from . import models
from .views import router as api_router


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(api_router, prefix="/views")


@app.get("/")
def root():
    return {"Message": "Welcome to our Book Giveaway API"}
