from fastapi import FastAPI, HTTPException
from typing import List, Optional
from model import Customer, Policy
from data import get_all_customers, get_all_policies, get_policy_by_id, get_policies_by_customer_id, init_database, init_sample_data

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_database()
    await init_sample_data()


@app.get("/customers", response_model=List[Customer])
async def get_customers():
    return await get_all_customers()


@app.get("/policies", response_model=List[Policy])
async def get_policies():
    return await get_all_policies()


@app.get("/policies/{policy_id}", response_model=Policy)
async def get_policy(policy_id: int):
    policy = await get_policy_by_id(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@app.get("/customers/{customer_id}/policies", response_model=List[Policy])
async def get_customer_policies(customer_id: int):
    policies = await get_policies_by_customer_id(customer_id)
    return policies
