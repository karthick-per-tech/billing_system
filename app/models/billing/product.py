from sqlalchemy import Float, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "billing"}

    product_pk: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    product_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    available_stocks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    unit_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    tax_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    bill_items = relationship(
        "BillItem",
        back_populates="product",
    )