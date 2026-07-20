from fastapi import Depends, APIRouter

from app.core.dependencies.billing_dependencies_container import (
    BillingSystemDependencyContainer,
    get_billing_system_container
)
from app.schemas.generate_bill import BillingRequestDTO
router = APIRouter(
    tags=["Billing System"]
)

@router.get(
        "/get_all_products_list",
        name='get all products',
        description="get all the product details from database",
        )

async def get_all_products(
    c:BillingSystemDependencyContainer = Depends(get_billing_system_container)
):
    return await c.service.get_all_products()

@router.post(
    "/generate_bills",
    name="generate bill",
    description="generate bill for the customer"
)
async def generate_bill(
    data : BillingRequestDTO,c:BillingSystemDependencyContainer = Depends(get_billing_system_container)
):
    return await c.service.generate_bill(data)