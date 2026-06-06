from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from uuid import UUID, uuid4
from datetime import datetime

class ImageSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    url: str
    ordering: int

class CharacteristicSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    value: str

class ProductCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=5000)
    category_id: UUID
    slug: Optional[str] = None
    images: List[ImageSchema] = Field(..., min_length=1)
    characteristics: Optional[List[CharacteristicSchema]] = []
    
    @field_validator('images')
    @classmethod
    def images_not_empty(cls, v):
        if not v:
            raise ValueError('At least one image is required')
        return v

class ProductResponse(BaseModel):
    id: UUID
    seller_id: UUID
    category_id: UUID
    title: str
    slug: str
    description: str
    status: str
    deleted: bool
    blocked: bool
    blocking_reason_id: UUID
    moderator_comment: str
    images: List[ImageSchema]
    characteristics: List[CharacteristicSchema]
    skus: List[Any]
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}