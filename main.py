import zoneinfo
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from models import Customer, CustomerCreate, Transaction, Invoice, CustomerBase
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

@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesnt exist")
    return customer_db

@app.patch("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer_data: CustomerBase, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesnt exist")
    customerData = customer_data.model_dump()
    customer_db.sqlmodel_update(customerData)
    session.commit()
    session.refresh(customer_db)
    return customer_db


@app.delete("/customers/{customer_id}", response_model=Customer)
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesnt exist")
    session.delete(customer_db)
    session.commit()
    return {"detail": "Customer deleted successfully"}


@app.get("/customers/", response_model=list[Customer])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()
    

@app.post("/transactions/")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices/")
async def create_invoices(invoice_data: Invoice):
    return invoice_data