from fastapi import APIRouter

router = APIRouter()


@router.get("/analytics")
async def get_analytics():
    """Возвращает аналитические данные (заглушка)."""
    return {"metrics": {}}
