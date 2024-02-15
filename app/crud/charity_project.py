from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            charity_project_name: int,
            session: AsyncSession,
    ) -> Optional[int]:
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        charity_project_id = charity_project_id.scalars().first()
        return charity_project_id


charity_project_crud = CRUDCharityProject(CharityProject)
