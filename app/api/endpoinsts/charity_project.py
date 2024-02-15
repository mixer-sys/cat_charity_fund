from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_name_duplicate,
    is_fully_invested,
    is_partially_invested,
    is_invested_amount_more_full,
    is_closed
)
from app.core.db import get_async_session
# Вместо импортов 6 функций импортируйте объект charity_project_crud.
from app.crud.charity_project import charity_project_crud
from app.core.user import current_superuser
from app.services.invest import invest
from app.schemas.charity_project import (
    CharityProjectBase,
    CharityProjectUpdateResponse,
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDelete,
    CharityProjectDB
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)

    charity_project = await charity_project_crud.create(charity_project, session)
    await invest(charity_project, session)
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectUpdateResponse,
    response_model_exclude_none=False,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await is_fully_invested(project_id, session)
    await is_invested_amount_more_full(obj_in, charity_project, session)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    # Замените вызов функции на вызов метода.
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDelete,
    response_model_exclude_none=False,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(charity_project_id, session)

    await is_closed(charity_project_id, session)
    await is_fully_invested(charity_project_id, session)
    await is_partially_invested(charity_project_id, session)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project