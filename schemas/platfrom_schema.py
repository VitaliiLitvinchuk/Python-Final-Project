from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional


class PlatformSchema(BaseModel):
    name: str
    base_url: HttpUrl
    search_url_template: Optional[HttpUrl] = None

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Назва має бути від 1 до 100 символів")
        return value

    @field_validator("search_url_template")
    def validate_search_url_template(
        cls, value: Optional[HttpUrl]
    ) -> Optional[HttpUrl]:
        if value and len(str(value)) > 512:
            raise ValueError("Шаблон URL пошуків не повинен перевищувати 512 символів")
        if value and "{search}" not in str(value):
            raise ValueError("Шаблон URL пошуків повинен містити {search}")
        return value

    class Config:
        from_attributes = True
