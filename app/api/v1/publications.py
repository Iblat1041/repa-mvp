from fastapi import APIRouter

router = APIRouter()


@router.get("/publications")
async def list_publications():
    """Возвращает список публикаций (заглушка)."""
    return {"items": []}
