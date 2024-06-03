from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session

from core import models
from core.database import engine
from crud.Auth import register_admin
from crud.Users import get_user_by_username
from routes import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        if not get_user_by_username(db, "admin"):
            register_admin(db, "admin", "0000", "Admin User")

    # Load the ML model
    yield


app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8000, reload=True)
