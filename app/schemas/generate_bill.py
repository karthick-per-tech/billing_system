from typing import Any

from pydantic import BaseModel, EmailStr, Field


class BillingRequestDTO(BaseModel):
    customer_email: EmailStr
    bill_section: dict[str, Any] = Field(
        description="Billing details in JSON format"
    )
    denomination: dict[str, Any] = Field(
        description="Cash denomination details in JSON format"
    )
    cash_paid: float = Field(
        ge=0,
        description="Amount paid by the customer"
    )