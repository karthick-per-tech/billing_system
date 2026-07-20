from sqlalchemy import select

from app.core.database.db_connection import async_session_factory
from app.models.billing.product import Product
from app.utils.seed.products import PRODUCTS


async def seed_products():
    async with async_session_factory() as session:
        result = await session.execute(select(Product).limit(1))
        if result.scalar_one_or_none():
            return
        session.add_all(
            [Product(**product) for product in PRODUCTS]
        )
        await session.commit()
