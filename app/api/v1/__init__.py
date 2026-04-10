from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.events import router as events_router


router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(events_router)
