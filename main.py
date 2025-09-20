from fastapi import FastAPI, HTTPException
from typing import List, Optional
from decimal import Decimal
from model import Customer, Policy
from data import get_all_customers, get_customer_by_id, get_customers_by_state, get_all_policies, get_policy_by_id, get_policies_by_customer_id, init_database, init_sample_data, ensure_fresh_sample_data

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_database()
    await init_sample_data()


@app.get("/customers", response_model=List[Customer])
async def get_customers():
    await ensure_fresh_sample_data()
    return await get_all_customers()


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    await ensure_fresh_sample_data()
    customer = await get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer



@app.get("/policies/{policy_id}", response_model=Policy)
async def get_policy(policy_id: int):
    await ensure_fresh_sample_data()
    policy = await get_policy_by_id(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


@app.get("/customers/{customer_id}/policies", response_model=List[Policy])
async def get_customer_policies(customer_id: int):
    await ensure_fresh_sample_data()
    policies = await get_policies_by_customer_id(customer_id)
    return policies


@app.get("/customers/state/{state}", response_model=List[Customer])
async def get_customers_in_state(state: str):
    await ensure_fresh_sample_data()
    customers = await get_customers_by_state(state)
    return customers


@app.get("/customers/{customer_id}/total-premium")
async def get_customer_total_premium(customer_id: int):
    await ensure_fresh_sample_data()
    
    customer = await get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    policies = await get_policies_by_customer_id(customer_id)
    total_premium = sum(policy.premium for policy in policies)
    
    return {"customer_id": customer_id, "total_premium": total_premium}
