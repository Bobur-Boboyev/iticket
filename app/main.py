from fastapi import FastAPI

from app.api import router
from app.db.init_db import init_db


app = FastAPI(title="Iticket API")
app.include_router(router)

# init_db()


@app.get("/")
async def root_view():
    return {"message": "project is running..."}
