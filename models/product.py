from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, Optional

from .base import Base


class Product(Base):
    """
    Модель для загального опису товару, який відстежується.
    Це "глобальна" сутність, до якої прив'язуються дані з різних платформ.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    global_query_name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(Text)

    scraped_data: Mapped[List["ScrapedProductData"]] = relationship(  # noqa: F821 # type: ignore
        back_populates="product", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, global_query_name='{self.global_query_name}')>"
