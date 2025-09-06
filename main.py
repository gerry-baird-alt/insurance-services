from fastapi import FastAPI
from typing import List
from model import Customer
from data import get_all_customers, init_database, init_sample_data

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_database()
    await init_sample_data()


@app.get("/customers", response_model=List[Customer])
async def get_customers():
    return await get_all_customers()
