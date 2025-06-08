from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

import datetime
from typing import Dict, List, Optional

from .base import Base


class RegressionModel(Base):
    """
    Модель для зберігання результатів навченої моделі лінійної регресії.
    """

    __tablename__ = "regression_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_variable: Mapped[str] = mapped_column(
        String(100), nullable=False, default="search_position"
    )

    feature_variables: Mapped[List[str]] = mapped_column(JSON)
    coefficients_json: Mapped[Dict[str, float]] = mapped_column(JSON)

    intercept: Mapped[Optional[float]] = mapped_column(Float)
    r_squared: Mapped[Optional[float]] = mapped_column(Float)

    last_trained_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    platform_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("platforms.id"), index=True
    )

    platform: Mapped[Optional["Platform"]] = relationship(  # noqa: F821 # type: ignore
        back_populates="regression_models"
    )

    def __repr__(self) -> str:
        return f"<RegressionModel(id={self.id}, name='{self.name}', r_squared={self.r_squared})>"
