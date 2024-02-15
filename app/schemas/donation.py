from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, root_validator, validator, Field


FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class DonationBase(BaseModel):
    create_date: datetime = Field(..., example=FROM_TIME)
    #close_date: Optional[datetime] = Field(..., example=TO_TIME)

    class Config:
        extra = Extra.forbid


class DonationUpdate(DonationBase):
    ...
    #@validator('create_date')
    #def check_from_reserve_later_than_now(cls, value):
    #    if value <= datetime.now():
    #        raise ValueError(
    #            'Время начала бронирования '
    #            'не может быть меньше текущего времени'
    #        )
    #    return value

    #@root_validator(skip_on_failure=True)
    #def check_from_reserve_before_to_reserve(cls, values):
    #    if values['from_reserve'] >= values['to_reserve']:
    #        raise ValueError(
    #            'Время начала бронирования '
    #            'не может быть больше времени окончания'
    #        )
    #    return values


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
