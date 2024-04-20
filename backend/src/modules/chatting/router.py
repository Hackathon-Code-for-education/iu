__all__ = ["router"]

from fastapi import APIRouter
from src.modules.chatting.chat_queue.router import router as chat_queue_router
from src.modules.chatting.dialog.router import router as dialog_router

router = APIRouter(prefix="/chatting", tags=["Chatting"])

router.include_router(chat_queue_router)
router.include_router(dialog_router)
