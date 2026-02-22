from pydantic import BaseModel
from typing import Optional

class InvoiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    amount: float

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int

    class Config:
        from_attributes = True