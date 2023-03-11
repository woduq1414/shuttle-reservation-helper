from fastapi import APIRouter, FastAPI
from api.shuttle.views import router as shuttle_router
from api.reservation.views import router as reservation_router

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

router.include_router(shuttle_router, prefix="/shuttle", tags=["shuttle"])
router.include_router(reservation_router, prefix="/reservation", tags=["reservation"])


@router.get("/")
async def root():
    return {"message": "Hello API!"}