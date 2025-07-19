from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

from app.db import Base, engine
from app.routes import router as client_router

load_dotenv()

app = FastAPI(title="API Gestion des Clients")


@asynccontextmanager
async def lifespan():
    Base.metadata.create_all(bind=engine)
    yield


app.include_router(client_router)
