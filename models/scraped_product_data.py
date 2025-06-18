from sqlalchemy import DateTime, Float, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

import datetime
from decimal import Decimal

from .base import Base


class ScrapedProductData(Base):
    """
    Модель для зберігання даних, зібраних скрейпером для конкретного товару
    на конкретній платформі в певний момент часу.
    """

    __tablename__ = "scraped_product_data"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False, index=True
    )
    platform_id: Mapped[int] = mapped_column(
        ForeignKey("platforms.id"), nullable=False, index=True
    )

    url_on_platform: Mapped[str] = mapped_column(String(1024), nullable=False)
    name_on_platform: Mapped[str] = mapped_column(String(512), nullable=False)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False)

    rating: Mapped[float] = mapped_column(Float, nullable=False)
    reviews_count: Mapped[int] = mapped_column(Integer, nullable=False)
    availability_status: Mapped[str] = mapped_column(String(100), nullable=False)
    search_position: Mapped[int] = mapped_column(Integer, nullable=False)

    scraped_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    product: Mapped["Product"] = relationship(back_populates="scraped_data")  # noqa: F821 # type: ignore
    platform: Mapped["Platform"] = relationship(back_populates="scraped_data")  # noqa: F821 # type: ignore

    def __repr__(self) -> str:
        return f"<ScrapedProductData(id={self.id}, name='{self.name_on_platform}', price={self.price})>"
