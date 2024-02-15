from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.crud.base import CRUDBase
# from app.models.reservation import Donation
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_donations_at_the_same_time(
            self,
            *,
            create_date: datetime,
            close_date: datetime,
            charity_project_id: int,

            donation_id: Optional[int] = None,
            session: AsyncSession,
    ) -> list[Donation]:
        select_stmt = select(Donation).where(
            Donation.charity_project_id == charity_project_id,
            and_(
                create_date <= Donation.create_date,
                close_date >= Donation.close_date
            )
        )

        if donation_id is not None:
            select_stmt = select_stmt.where(
                Donation.id != donation_id
            )

        donations = await session.execute(select_stmt)
        donations = donations.scalars().all()
        return donations

    async def get_future_donations_for_room(
            self,
            room_id: int,
            session: AsyncSession,
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.charity_project_id == room_id,

                Donation.to_reserve > datetime.now()
            )
        )
        donations = donations.scalars().all()
        return donations

    async def get_by_user(
            self, session: AsyncSession, user: User
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()

donation_crud = CRUDDonation(Donation)  # noqa
