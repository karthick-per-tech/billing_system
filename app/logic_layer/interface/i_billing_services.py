from abc import ABC, abstractmethod


class IBillingSystemServices(ABC):
    
    @abstractmethod
    async def get_all_products(self):
        raise NotImplementedError
    
    @abstractmethod
    async def generate_bill(self,data):
        raise NotImplementedError