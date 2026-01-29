import zoneinfo
from datetime import datetime

from fastapi import FastAPI
from models import Transaction, Invoice
from db import  SessionDep, create_all_tables
from sqlmodel import select
from .routers import customers, transactions, invoices, plans

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)
app.include_router(invoices.router)

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
   
