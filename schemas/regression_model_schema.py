from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict


class RegressionModelSchema(BaseModel):
    name: str
    target_variable: str
    feature_variables: List[str]
    coefficients_json: Dict[str, float]
    intercept: Optional[float] = None
    r_squared: Optional[float] = None
    platform_id: Optional[int] = None

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if len(value) < 1 or len(value) > 255:
            raise ValueError("Назва має бути від 1 до 255 символів")
        return value

    @field_validator("target_variable")
    def validate_target_variable(cls, value: str) -> str:
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Значення цілевої змінної має бути від 1 до 100 символів")
        return value

    @field_validator("feature_variables")
    def validate_feature_variables(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("Значення списку змінних не може бути порожнім")
        for var in value:
            if len(var) < 1 or len(var) > 100:
                raise ValueError("Значення змінної має бути від 1 до 100 символів")
        return value

    @field_validator("r_squared")
    def validate_r_squared(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and (value < 0 or value > 1):
            raise ValueError("Значення R^2 має бути від 0 до 1")
        return value

    @field_validator("platform_id")
    def validate_platform_id(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value <= 0:
            raise ValueError("ID платформи має бути більше 0")
        return value

    class Config:
        from_attributes = True
