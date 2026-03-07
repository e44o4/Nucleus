from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.tenant import Tenant

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tenants")
def create_tenant(name: str, db: Session = Depends(get_db)):

    tenant = Tenant(name=name)

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant


@router.get("/tenants")
def list_tenants(db: Session = Depends(get_db)):

    tenants = db.query(Tenant).all()

    return tenants