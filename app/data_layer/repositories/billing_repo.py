from decimal import Decimal, ROUND_HALF_UP
import traceback
import asyncio
import logging

from fastapi import HTTPException, status
from fastapi import BackgroundTasks
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_layer.interface.i_billing_repo import IBillingSystemRepositories
from app.models.billing.product import Product
from app.schemas.generate_bill import BillingRequestDTO
from app.utils.helpers.calculate_denomination import calculate_cash_paid, calculate_change
from app.models.billing.customer import Customer
from app.models.billing.bill import Bill
from app.models.billing.bill_items import BillItem
from app.utils.helpers.email_service import send_bill_email

logger = logging.getLogger(__name__)

_background_tasks: set[asyncio.Task] = set()

def _schedule_background_email(to_email: str, items: list, summary: dict) -> None:
    task = asyncio.create_task(send_bill_email(to_email, items, summary))
    _background_tasks.add(task)
    task.add_done_callback(_on_email_task_done)


def _on_email_task_done(task: asyncio.Task) -> None:
    _background_tasks.discard(task)
    try:
        task.result()  # re-raises if send_bill_email threw
    except Exception:
        logger.error("Background bill-email task failed:\n%s", traceback.format_exc())



class BillingSystemRepositories(IBillingSystemRepositories):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_products(self):
        result = await self.db.execute(
            select(Product).order_by(Product.product_id)
        )
        return result.scalars().all()
    
    async def save_invoice_details(
    self,
    email_id: str,
    summary: dict,
    items: list,
):
        try:
            async with self.db.begin():
                # Customer (Get or Create)
                result = await self.db.execute(
                    select(Customer).where(Customer.email_id == email_id)
                )
                customer = result.scalar_one_or_none()

                if customer is None:
                    customer = Customer(
                        email_id=email_id,
                    )
                    self.db.add(customer)
                    await self.db.flush()
                    print("Customer PK:", customer.customer_pk)


                customer_pk = customer.customer_pk

                # insert bill details
                bill = Bill(
                    customer_fk=customer_pk,
                    total_price_without_tax=summary["total_price_without_tax"],
                    total_tax_payable=summary["total_tax_payable"],
                    net_price_of_the_purchased_item=summary[
                        "net_price_of_purchased_items"
                    ],
                    rounded_down_value=summary[
                        "rounded_value_of_purchased_items"
                    ],
                    balance_payable_to_the_customer=summary.get(
                        "balance_payable_to_customer",
                        0,
                    ),
                )

                self.db.add(bill)
                await self.db.flush()
                bill_pk = bill.bill_pk

                # Bill Items
                bill_items = []
                for item in items:
                    bill_items.append(
                        BillItem(
                            bill_fk=bill_pk,
                            product_fk=item["product_uuid"],
                            unit_price=item["unit_price"],
                            quantity=item["quantity"],
                            purchased_price=item["unit_price"],
                            tax_for_item=item["tax_percentage"],
                            tax_payable_for_items=item["tax_amount"],
                            total_price_of_the_item=item["total"],
                        )
                    )

                self.db.add_all(bill_items)
            return {
                "customer_pk": str(customer_pk),
                "bill_pk": str(bill_pk),
            }

        except SQLAlchemyError as e:
            await self.db.rollback()
            traceback.print_exc()
            raise

        except Exception:
            await self.db.rollback()
            raise
    
    async def generate_bill(self,data:BillingRequestDTO):
        email = data.customer_email
        bill = data.bill_section
        denomination = data.denomination

        calculated_cash = await calculate_cash_paid(denomination)

        entered_cash = Decimal(str(data.cash_paid))

        if calculated_cash != entered_cash:
            raise  HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Cash paid does not match denomination.",
                    "cash_paid": float(entered_cash),
                    "denomination_total": float(calculated_cash),
                },
            )
    
        cash_paid = calculated_cash
        items = []

        total_without_tax = Decimal("0")
        total_tax = Decimal("0")

        for product in bill["items"]:

            quantity = Decimal(str(product["quantity"]))
            unit_price = Decimal(str(product["unit_price"]))
            tax_percentage = Decimal(str(product["tax_percentage"]))

            subtotal = quantity * unit_price

            tax_amount = (
                subtotal * tax_percentage
            ) / Decimal("100")

            total = subtotal + tax_amount

            total_without_tax += subtotal
            total_tax += tax_amount

            items.append(
                {
                    "product_id": product["product_id"],
                    "product_uuid": product["product_uuid"],
                    "product_name": product["product_name"],
                    "quantity": int(quantity),
                    "unit_price": float(unit_price),
                    "tax_percentage": float(tax_percentage),
                    "subtotal": float(subtotal),
                    "tax_amount": float(tax_amount),
                    "total": float(total),
                }
            )

        net_price = total_without_tax + total_tax

        rounded_price = net_price.quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )

        balance = cash_paid - rounded_price

        summary = {
            "total_price_without_tax": float(total_without_tax),
            "total_tax_payable": float(total_tax),
            "net_price_of_purchased_items": float(net_price),
            "rounded_value_of_purchased_items": float(rounded_price),
            "cash_paid": float(cash_paid),
        }


        if balance > 0:
            summary["balance_payable_to_customer"] = float(balance)
            summary["return_denomination"] = await calculate_change(balance)
       
        elif balance < 0:
            pending_amount = abs(balance)
            summary["pending_amount"] = float(pending_amount)
            summary["denomination_to_be_paid"] = await calculate_change(
                pending_amount
            )
        else:
            summary["balance_payable_to_customer"] = 0
            summary["return_denomination"] = {}

        # save invoice details in the database
        await self.save_invoice_details(email, summary,items)
        # background task to send email
        _schedule_background_email(email, items, summary)

        return {
            "customer_email": email,
            "items": items,
            "summary": summary,
        }
    
