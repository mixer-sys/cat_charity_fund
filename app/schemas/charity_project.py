from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator, Extra, root_validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(..., min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[int]
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]

    class Config:
        extra = Extra.forbid


class CharityProjectGet(BaseModel):
    ...


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=100)
    full_amount: int
    invested_amount: Optional[int]

    @validator('full_amount')
    def check_full_amount_more_one(cls, value):
        if value < 1:
            raise ValueError(
                'Требуемая сумма (full_amount)'
                ' проекта должна быть целочисленной'
                ' и больше 0.'
            )
        return value


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=100)
    full_amount: Optional[int] = Field(gt=0)

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if ('invested_amount', ) in values:
            if values['invested_amount'] > values['full_amount']:
                raise ValueError(
                    'Время начала бронирования '
                    'не может быть больше времени окончания'
                )
        return values

    class Config:
        extra = Extra.forbid


class CharityProjectUpdateResponse(BaseModel):
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


class CharityProjectDelete(BaseModel):
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    description: Optional[str]
    full_amount: Optional[int]
    fully_invested: bool = Field(None, )
    id: int
    invested_amount: Optional[int] = Field(...,)
    name: Optional[str]

    class Config:
        orm_mode = True

    @validator('fully_invested')
    def set_fully_invested(cls, name):
        return name or False

    @validator('invested_amount')
    def set_invested_amount(cls, name):
        return name or 0