from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: int = Field(None, min=1)
    invested_amount: int = Field(None, min=1)
    fully_invested: bool = Field(False)
    create_date: datetime = Field(datetime.now())
    close_date: datetime = Field(None)