from pydantic import BaseModel, field_validator
from typing import Optional


class ProductSchema(BaseModel):
    global_query_name: str
    description: Optional[str] = None

    @field_validator("global_query_name")
    def validate_global_query_name(cls, value: str) -> str:
        if len(value) < 1 or len(value) > 255:
            raise ValueError("Global query name must be between 1 and 255 characters")
        return value

    @field_validator("description")
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value) > 10000:
            raise ValueError("Description must not exceed 10000 characters")
        return value

    class Config:
        from_attributes = True
