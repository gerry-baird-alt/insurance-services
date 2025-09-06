from pydantic import BaseModel
from datetime import date


class Customer(BaseModel):
    name: str
    date_of_birth: date
    email: str
    address: str
    state: str