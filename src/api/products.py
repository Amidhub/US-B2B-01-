from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from src.database import get_db
from src.schemas.product import ProductCreateRequest, ProductResponse
from src.services.product_service import ProductService
from src.dependencies.auth import get_current_seller_id

router = APIRouter(prefix="/api/v1/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    product_data: ProductCreateRequest,
    seller_id: UUID = Depends(get_current_seller_id),
    db: Session = Depends(get_db)
):
    if not product_data.images:
        raise HTTPException(400, {"code": "INVALID_REQUEST", "message": "At least one image is required"})
    
    service = ProductService(db)
    product = service.create_product(seller_id, product_data)
    return product