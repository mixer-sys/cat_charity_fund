from fastapi import APIRouter

from app.api.endpoinsts import (
    charityproject_router
)


main_router = APIRouter()
main_router.include_router(
    charityproject_router, prefix='/charity_project', tags=['Charity project']
)

'''
main_router.include_router(
    reservation_router, prefix='/reservations', tags=['Reservations']
)


'''
