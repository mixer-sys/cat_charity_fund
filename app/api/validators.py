from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_name_duplicate(
        charity_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_charity_project_id_by_name(charity_name, session)
    if charity_project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def is_fully_invested(
        charity_project_id: int,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )


async def is_closed(
        charity_project_id: int,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def is_partially_invested(
        charity_project_id: int,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.invested_amount:
        if charity_project.invested_amount > 0:
            raise HTTPException(
                status_code=400,
                detail='В проект были внесены средства, не подлежит удалению!',
            )


async def is_invested_amount_more_full(
        obj_in: CharityProject,
        charity_project: CharityProject,
        session: AsyncSession
) -> None:

    if obj_in.full_amount and charity_project.invested_amount:
        if obj_in.full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=400,
                detail='При редактировании проекта  запрещено устанавливать требуемую сумму меньше внесённой.',
            )
