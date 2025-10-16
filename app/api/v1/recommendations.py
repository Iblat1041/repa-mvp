from fastapi import APIRouter

router = APIRouter()


@router.get("/recommendations")
async def get_recommendations():
    """Возвращает рекомендации от AI (заглушка)."""
    return {"advice": "Публикуйте в тематических СМИ для лучшего охвата."}
