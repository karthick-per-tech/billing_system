from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base


class Bill(Base):
    __tablename__ = "bill"
    __table_args__ = {"schema": "billing"}

    bill_pk: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    customer_fk: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("billing.customer.customer_pk"),
        nullable=False,
    )

    total_price_without_tax: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    total_tax_payable: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    net_price_of_the_purchased_item: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    rounded_down_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    balance_payable_to_the_customer: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone("UTC", func.now()),
        nullable=False,
    )

    customer = relationship(
        "Customer",
        back_populates="bills",
    )

    bill_items = relationship(
        "BillItem",
        back_populates="bill",
        cascade="all, delete-orphan",
    )