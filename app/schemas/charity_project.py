from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, root_validator, validator

from app.core.constants import (
    FULL_AMOUNT_SHOUL_BE_MORE_INVESTED_AMOUNT,
    FULL_AMOUNT_SHOUL_BE_POSITIVE_INT,
    MAX_LENGTH,
    MIN_LENGTH
)


class CharityProjectCreate(BaseModel):
    name: str = Field(
        ..., min_length=MIN_LENGTH, max_length=MAX_LENGTH
    )
    description: str = Field(
        ..., min_length=MIN_LENGTH, max_length=MAX_LENGTH
    )
    full_amount: int
    invested_amount: Optional[int]

    @validator('full_amount')
    def check_full_amount_more_one(cls, value):
        if value < 1:
            raise ValueError(
                FULL_AMOUNT_SHOUL_BE_POSITIVE_INT
            )
        return value


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MIN_LENGTH, max_length=MAX_LENGTH
    )
    description: Optional[str] = Field(
        None, min_length=MIN_LENGTH, max_length=MAX_LENGTH
    )
    full_amount: Optional[int] = Field(gt=0)

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if ('invested_amount', ) in values:
            if values.get('invested_amount') > values.get('full_amount'):
                raise ValueError(
                    FULL_AMOUNT_SHOUL_BE_MORE_INVESTED_AMOUNT
                )
        return values

    class Config:
        extra = Extra.forbid


class CharityProjectDB(BaseModel):
    id: int
    close_date: Optional[datetime]
    create_date: datetime
    description: Optional[str]
    full_amount: Optional[int]
    fully_invested: Optional[bool]
    invested_amount: Optional[int]
    name: Optional[str]

    class Config:
        orm_mode = True

    @validator('fully_invested')
    def set_fully_invested(cls, name):
        return name or False

    @validator('invested_amount')
    def set_invested_amount(cls, name):
        return name or 0
