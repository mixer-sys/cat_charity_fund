from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from app.core.constants import (
    FULL_AMOUNT_SHOUL_BE_POSITIVE_INT
)


class DonationCreate(BaseModel):
    full_amount: int
    comment: Optional[str]

    @validator('full_amount')
    def check_full_amount_more_one(cls, value):
        if value < 1:
            raise ValueError(
                FULL_AMOUNT_SHOUL_BE_POSITIVE_INT
            )
        return value


class DonationDB(BaseModel):
    comment: Optional[str]
    create_date: Optional[datetime]
    full_amount: Optional[int]
    id: int

    class Config:
        orm_mode = True


class DonationGetAll(DonationDB):
    full_amount: Optional[int]
    fully_invested: Optional[bool]
    id: int
    invested_amount: Optional[int]
    user_id: int

    @validator('fully_invested')
    def set_fully_invested(cls, name):
        return name or False

    @validator('invested_amount')
    def set_invested_amount(cls, name):
        return name or 0
