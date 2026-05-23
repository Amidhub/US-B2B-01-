from sqlalchemy.orm import Session
from uuid import UUID
from src.models.product import Product
from src.schemas.product import ProductCreateRequest

class ProductService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_product(self, seller_id: UUID, product_data: ProductCreateRequest) -> Product:
        slug = product_data.slug or product_data.title.lower().replace(" ", "-")[:255]
        
        product = Product(
            seller_id=seller_id,
            category_id=product_data.category_id,
            title=product_data.title,
            slug=slug,
            description=product_data.description,
            status="CREATED",
            deleted=False,
            blocked=False,
            images=[img.dict() for img in product_data.images],
            characteristics=[char.dict() for char in product_data.characteristics],
            skus=[]
        )
        
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        
        return product