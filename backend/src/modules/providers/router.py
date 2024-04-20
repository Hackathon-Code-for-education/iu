from fastapi import APIRouter

from src.modules.providers.credentials.router import router as credentials_router
from src.modules.providers.telegram.router import router as telegram_router

router = APIRouter(prefix="/providers", tags=["Providers"])

router.include_router(credentials_router)
router.include_router(telegram_router)
