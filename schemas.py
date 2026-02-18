from pydantic import BaseModel
from typing import Optional
from datetime import date

class ExpenseCreate(BaseModel):
    amount: float
    item: str
    paid_on: date
    category: str

class ExpenseResponse(BaseModel):
    id: str
    amount: float
    item: str
    paid_on: date
    category: str
    deleted: int
    created_at: str
    updated_at: str
    deleted_at: Optional[str]

#Optional is used to tell fastapi that user may or may not send this field for updating....
class UpdateExpenseModel(BaseModel):
    amount: Optional[float]=None
    item: Optional[str]=None
    paid_on: Optional[date]=None
    category: Optional[str]=None
