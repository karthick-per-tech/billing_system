from typing import Any, Optional

from pydantic import BaseModel


class ResponseModel(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None


