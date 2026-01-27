import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
    return {"message": "Hello, Luis!"}

country_timezones = {
    "CO": "America/Bogota",
    "US": "America/New_York",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "MX": "America/Mexico_City",
    "PE": "America/Lima",
    "CL": "America/Santiago",
    "VE": "America/Caracas",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    if not timezone_str:
        return {"error": "Invalid ISO code"}
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

db_customers: list[Customer] = []

@app.post("/customers/", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers/", response_model=list[Customer])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()
    


@app.get("/customer/{id_customer}", response_model=Customer)
async def get_customer(id_customer: int):
    return db_customers[id_customer]

@app.post("/transactions/")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices/")
async def create_invoices(invoice_data: Invoice):
    return invoice_data