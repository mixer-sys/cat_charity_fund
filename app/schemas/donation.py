from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, validator, Field


class DonationBase(BaseModel):
    create_date: datetime = Field(..., example=datetime.now())

    class Config:
        extra = Extra.forbid


class DonationUpdate(DonationBase):
    ...


class DonationCreate(BaseModel):
    full_amount: int
    comment: Optional[str]

    @validator('full_amount')
    def check_full_amount_more_one(cls, value):
        if value < 1:
            raise ValueError(
                'Требуемая сумма (full_amount)'
                ' проекта должна быть целочисленной'
                ' и больше 0.'
            )
        return value

    class Config:
        extra = Extra.forbid


class DonationCreateResponse(BaseModel):
    id: int
    full_amount: Optional[int]
    create_date: Optional[datetime]
    comment: Optional[str]

    class Config:
        orm_mode = True


class DonationGetAll(BaseModel):
    comment: Optional[str]
    create_date: Optional[datetime]
    full_amount: Optional[int]
    fully_invested: Optional[bool]
    id: int
    invested_amount: Optional[int]
    user_id: int

    class Config:
        orm_mode = True

    @validator('fully_invested')
    def set_fully_invested(cls, name):
        return name or False

    @validator('invested_amount')
    def set_invested_amount(cls, name):
        return name or 0


class DonationDB(DonationBase):
    comment: Optional[str]
    create_date: Optional[datetime]
    full_amount: Optional[int]
    id: int

    class Config:
        orm_mode = True
