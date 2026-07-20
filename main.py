from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.billing_router import router
from app.utils.seed.seed_products import seed_products


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_products()
    yield


app = FastAPI(
    title="Billing Management System",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1/billing_system")