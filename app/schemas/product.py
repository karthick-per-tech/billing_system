from uuid import UUID

from pydantic import BaseModel, ConfigDict

class ProductResponse(BaseModel):
    product_pk: UUID
    product_id: int
    product_name: str
    available_stocks: int
    unit_price: float
    tax_percentage: float

    model_config = ConfigDict(from_attributes=True)
