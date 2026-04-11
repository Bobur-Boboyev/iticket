from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.events import router as events_router
from app.api.v1.endpoints.orders import router as orders_router
from app.api.v1.endpoints.tickets import router as tickets_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.venue import router as venues_router


router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(events_router)
router.include_router(orders_router)
router.include_router(tickets_router)
router.include_router(categories_router)
router.include_router(venues_router)
