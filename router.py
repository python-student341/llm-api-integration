from fastapi import APIRouter

from backend.api.user_api import router as user_router
from backend.api.gemini_api import router as gemini_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(gemini_router)