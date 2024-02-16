from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


MODEL_CHOISE = {
    Donation: CharityProject,
    CharityProject: Donation
}


async def invest(
        obj: Union[Donation, CharityProject],
        session: AsyncSession,
) -> None:

    model = MODEL_CHOISE[type(obj)]
    donat = obj
    projects = await session.execute(
        select(model).where(
            model.close_date == None  # noqa
        ).order_by(
            model.create_date
        )
    )
    projects = projects.scalars().all()

    for project in projects:
        if project.invested_amount is None:
            project.invested_amount = 0

        if donat.full_amount != donat.invested_amount:

            project_remained_amount = project.full_amount - project.invested_amount
            donat_remained_amount = donat.full_amount - donat.invested_amount

            if donat_remained_amount < project_remained_amount:
                project.invested_amount += donat_remained_amount
                donat.invested_amount += donat_remained_amount
            else:
                project.invested_amount += project_remained_amount
                donat.invested_amount += project_remained_amount

        if project.full_amount == project.invested_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
        if donat.full_amount == donat.invested_amount:
            donat.fully_invested = True
            donat.close_date = datetime.now()

    session.add(donat)
    session.add_all(projects)
    await session.commit()
    await session.refresh(donat)
    for project in projects:
        await session.refresh(project)
