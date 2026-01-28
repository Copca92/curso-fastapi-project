
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from models import Customer, CustomerCreate, CustomerUpdate
from db import SessionDep

router = APIRouter()

@router.post("/customers/", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesnt exist")
    return customer_db

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesnt exist")
    
    customer_data_dic = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dic)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return {"detail": "Customer updated successfully"}


@router.delete("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesnt exist")
    session.delete(customer_db)
    session.commit()
    return {"detail": "Customer deleted successfully"}


@router.get("/customers/", response_model=list[Customer], tags=["customers"])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()