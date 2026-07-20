from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.db_connection import get_db_session
from app.data_layer.interface.i_billing_repo import IBillingSystemRepositories
from app.data_layer.repositories.billing_repo import BillingSystemRepositories
from app.logic_layer.interface.i_billing_services import IBillingSystemServices
from app.logic_layer.services.billing_services import BillingSystemServices


class BillingSystemDependencyContainer:
    def __init__(self,db:AsyncSession):
        self.repo:IBillingSystemRepositories = BillingSystemRepositories(db)
        self.service:IBillingSystemServices = BillingSystemServices(db,self.repo)

def get_billing_system_container(
        db:AsyncSession = Depends(get_db_session),
) -> BillingSystemDependencyContainer:
    return BillingSystemDependencyContainer(db)