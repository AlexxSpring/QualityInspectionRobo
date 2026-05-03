from fastapi import APIRouter

from logic.database import get_recent_logs

router = APIRouter()

@router.get("")
async def fetch_logs(limit: int = 10):
    return get_recent_logs(limit)
