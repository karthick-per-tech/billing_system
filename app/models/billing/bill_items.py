from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base


class BillItem(Base):
    __tablename__ = "bill_item"
    __table_args__ = {"schema": "billing"}

    bill_item_pk: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    bill_fk: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("billing.bill.bill_pk"),
        nullable=False,
    )

    product_fk: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("billing.product.product_pk"),
        nullable=False,
    )

    unit_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    purchased_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    tax_for_item: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    tax_payable_for_items: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    total_price_of_the_item: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone("UTC", func.now()),
        nullable=False,
    )

    bill = relationship(
        "Bill",
        back_populates="bill_items",
    )

    product = relationship(
        "Product",
        back_populates="bill_items",
    )