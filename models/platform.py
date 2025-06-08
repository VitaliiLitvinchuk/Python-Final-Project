from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, Optional

from .base import Base


class Platform(Base):
    """
    Модель для опису платформи/маркетплейсу.
    Зберігає інформацію про назву, базову URL-адресу та шаблон для пошуку.
    """

    __tablename__ = "platforms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    base_url: Mapped[str] = mapped_column(String(255), nullable=False)
    search_url_template: Mapped[Optional[str]] = mapped_column(String(512))

    scraped_data: Mapped[List["ScrapedProductData"]] = relationship(  # noqa: F821 # type: ignore
        back_populates="platform", cascade="all, delete-orphan"
    )
    regression_models: Mapped[List["RegressionModel"]] = relationship(  # noqa: F821 # type: ignore
        back_populates="platform", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Platform(id={self.id}, name='{self.name}')>"
