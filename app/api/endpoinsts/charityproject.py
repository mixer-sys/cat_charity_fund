from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_charityproject_exists
from app.core.db import get_async_session
# Вместо импортов 6 функций импортируйте объект meeting_room_crud.
from app.crud.charityproject import charityproject_crud
from app.core.user import current_superuser

from app.schemas.charityproject import (
    CharityProjectBase
)

router = APIRouter()


@router.get(
    '/{charityproject_id}/charity_project',
    response_model=list[CharityProjectBase],
    response_model_exclude={'user_id'},
)
async def get_charityprojects(
    charityproject_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await check_charityproject_exists(charityproject_id, session)
    charityprojects = await charityproject_crud.get_charityproject_id_by_name(
        charityproject_id=charityproject_id,
        session=session
    )
    return charityprojects
