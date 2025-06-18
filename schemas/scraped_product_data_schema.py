from pydantic import BaseModel, HttpUrl, field_validator
from decimal import Decimal


class ScrapedProductDataSchema(BaseModel):
    product_id: int
    platform_id: int
    url_on_platform: HttpUrl
    name_on_platform: str
    price: Decimal
    currency: str
    rating: float
    reviews_count: int
    availability_status: str
    search_position: int

    @field_validator("product_id", "platform_id")
    def validate_positive_id(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("ID повинен бути позитивним")
        return value

    @field_validator("name_on_platform")
    def validate_name_on_platform(cls, value: str) -> str:
        if len(value) < 1 or len(value) > 512:
            raise ValueError("Назва на платформі повинна бути між 1 та 512 символами")
        return value

    @field_validator("price")
    def validate_price(cls, value: Decimal) -> Decimal:
        if value is not None and value < 0:
            raise ValueError("Ціна повинна бути не від'ємною")
        return value

    @field_validator("currency")
    def validate_currency(cls, value: str) -> str:
        if value and len(value) > 10:
            raise ValueError("Код валюти не повинен перевищувати 10 символів")
        if value and not value.isalpha():
            raise ValueError("Код валюти повинен складатися тільки з літер")
        return value

    @field_validator("rating")
    def validate_rating(cls, value: float) -> float:
        if value is not None and (value < 0 or value > 5):
            raise ValueError("Рейтинг повинен бути між 0 та 5")
        return value

    @field_validator("reviews_count")
    def validate_reviews_count(cls, value: int) -> int:
        if value is not None and value < 0:
            raise ValueError("Кількість відгуків повинна бути не від'ємною")
        return value

    @field_validator("availability_status")
    def validate_availability_status(cls, value: str) -> str:
        if value and len(value) > 100:
            raise ValueError("Статус доступності не повинен перевищувати 100 символів")
        return value

    @field_validator("search_position")
    def validate_search_position(cls, value: int) -> int:
        if value is not None and value < 0:
            raise ValueError("Позиція пошуку повинна бути не від'ємною")
        return value

    class Config:
        from_attributes = True
