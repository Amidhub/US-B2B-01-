from fastapi import Depends, HTTPException
from uuid import UUID

async def get_current_seller_id() -> UUID:
    # ВРЕМЕННО: для тестов просто возвращаем фиксированный ID
    return UUID("123e4567-e89b-12d3-a456-426614174000")