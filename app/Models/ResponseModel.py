from pydantic import BaseModel 
from typing import Any, Optional
class ResponseModel(BaseModel):
    success: bool = False
    message: str
    status_code: int = 200
    data: Optional[Any] = None