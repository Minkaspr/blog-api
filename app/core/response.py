from enum import Enum
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel

class ApiStatus(str, Enum):
  SUCCESS = "success"
  ERROR = "error"

T = TypeVar("T")

class ApiFieldError(BaseModel):
  field: str
  message: str

class ApiResponse(BaseModel, Generic[T]):
  status: ApiStatus
  message: str
  data: Optional[T] = None
  error: Optional[List[ApiFieldError]] = None
