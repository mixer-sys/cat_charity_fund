from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    INVESTED_CANT_DELETE,
    PROJECT_NAME_EXISTS,
    PROJECT_NOT_FOUND,
    NOT_PERMIT_CLOSED_PROJECT,
    NOT_PERMIT_FULL_AMOUNT_MORE_INVESTE_AMOUNT
)
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return charity_project


async def check_name_duplicate(
        charity_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = (
        await charity_project_crud.get_charity_project_id_by_name(
            charity_name, session)
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_NAME_EXISTS,
        )


async def is_fully_invested(
        charity_project_id: int,
        session: AsyncSession
) -> None:
    charity_project = (
        await charity_project_crud.get(charity_project_id, session)
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NOT_PERMIT_CLOSED_PROJECT,
        )


async def is_closed(
        charity_project_id: int,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVESTED_CANT_DELETE,
        )


async def is_partially_invested(
        charity_project_id: int,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id, session)
    if charity_project.invested_amount:
        if charity_project.invested_amount > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=INVESTED_CANT_DELETE,
            )


async def is_invested_amount_more_full(
        obj_in: CharityProject,
        charity_project: CharityProject,
        session: AsyncSession
) -> None:

    if obj_in.full_amount and charity_project.invested_amount:
        if obj_in.full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=NOT_PERMIT_FULL_AMOUNT_MORE_INVESTE_AMOUNT,
            )
