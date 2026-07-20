from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.logic_layer.interface.i_billing_services import IBillingSystemServices
from app.data_layer.interface.i_billing_repo import IBillingSystemRepositories
from app.utils.enum.message import MessageResponse
from app.utils.response.response import ResponseModel
from app.schemas.product import ProductResponse

class BillingSystemServices(IBillingSystemServices):
    def __init__(self, db: AsyncSession, repo: IBillingSystemRepositories):
        self.db = db
        self.repository = repo

    async def get_all_products(self):
        try:
            products = await self.repository.get_all_products()

            if not products:
                return ResponseModel(
                    code=status.HTTP_200_OK,
                    message=MessageResponse.SUCCESS.value,
                    data="No Data Found",
                )

            return ResponseModel(
                code=status.HTTP_200_OK,
                message=MessageResponse.SUCCESS.value,
                data=[
                    ProductResponse.model_validate(product)
                    for product in products
                ],
            )

        except Exception:
            return ResponseModel(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=MessageResponse.ERROR.value,
                data=None,
            )
        
    async def generate_bill(self,data):
        try:
            generate_bill_records = await self.repository.generate_bill(data)
            return ResponseModel(
                code=status.HTTP_200_OK,
                message=MessageResponse.SUCCESS.value,
                data=generate_bill_records,
            )
        except HTTPException as exc:
            detail = exc.detail
            if isinstance(detail, dict):
                message = detail.get("message", MessageResponse.ERROR.value)
                payload = detail
            else:
                message = str(detail)
                payload = {"detail": detail}

            return ResponseModel(
                code=exc.status_code,
                message=message,
                data=payload,
            )
        except Exception:
            return ResponseModel(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=MessageResponse.ERROR.value,
                data=None,
            )