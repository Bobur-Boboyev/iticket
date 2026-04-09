from fastapi import FastAPI

from app.db.init_db import init_db

init_db()
app = FastAPI(title="Iticket API")



@app.get("/")
async def root_view():
    return {"message": "project is running..."}
