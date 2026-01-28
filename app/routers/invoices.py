
from fastapi import APIRouter
from models import Invoice


router = APIRouter()

@router.post("/invoices/", tags=["invoices"])
async def create_invoices(invoice_data: Invoice):
    return invoice_data