from typing import Annotated, List, Optional
from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from db import SessionContext
from models.scraped_product_data import ScrapedProductData
from decimal import Decimal


class ScrapedProductDataRepository:
    def __init__(self, session: SessionContext):
        self.session = session

    async def get_scraped_product_data(self) -> List[ScrapedProductData]:
        query = select(ScrapedProductData)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Optional[ScrapedProductData]:
        query = select(ScrapedProductData).where(ScrapedProductData.id == id)
        result = await self.session.execute(query)
        return result.scalar()

    async def create_scraped_product_data(
        self,
        product_id: int,
        platform_id: int,
        url_on_platform: str,
        name_on_platform: str,
        price: Optional[Decimal] = None,
        currency: Optional[str] = None,
        rating: Optional[float] = None,
        reviews_count: Optional[int] = None,
        availability_status: Optional[str] = None,
        search_position: Optional[int] = None,
    ) -> ScrapedProductData:
        query = (
            insert(ScrapedProductData)
            .values(
                product_id=product_id,
                platform_id=platform_id,
                url_on_platform=url_on_platform,
                name_on_platform=name_on_platform,
                price=price,
                currency=currency,
                rating=rating,
                reviews_count=reviews_count,
                availability_status=availability_status,
                search_position=search_position,
            )
            .returning(ScrapedProductData)
        )
        result = await self.session.execute(query)
        scraped_data = result.scalar()
        await self.session.commit()
        await self.session.refresh(scraped_data)
        return scraped_data

    async def update_scraped_product_data(
        self,
        id: int,
        product_id: int,
        platform_id: int,
        url_on_platform: str,
        name_on_platform: str,
        price: Optional[Decimal] = None,
        currency: Optional[str] = None,
        rating: Optional[float] = None,
        reviews_count: Optional[int] = None,
        availability_status: Optional[str] = None,
        search_position: Optional[int] = None,
    ) -> ScrapedProductData:
        scraped_data = await self.get_by_id(id)
        if not scraped_data:
            raise ValueError(f"ScrapedProductData with id {id} not found")

        query = (
            update(ScrapedProductData)
            .where(ScrapedProductData.id == id)
            .values(
                product_id=product_id,
                platform_id=platform_id,
                url_on_platform=url_on_platform,
                name_on_platform=name_on_platform,
                price=price,
                currency=currency,
                rating=rating,
                reviews_count=reviews_count,
                availability_status=availability_status,
                search_position=search_position,
            )
            .returning(ScrapedProductData)
        )
        result = await self.session.execute(query)
        scraped_data = result.scalar()
        await self.session.commit()
        await self.session.refresh(scraped_data)
        return scraped_data

    async def delete_scraped_product_data(self, id: int) -> ScrapedProductData:
        scraped_data = await self.get_by_id(id)
        if not scraped_data:
            raise ValueError(f"ScrapedProductData with id {id} not found")

        query = (
            delete(ScrapedProductData)
            .where(ScrapedProductData.id == id)
            .returning(ScrapedProductData)
        )
        result = await self.session.execute(query)
        scraped_data = result.scalar()
        await self.session.commit()
        return scraped_data


ScrapedProductDataRepositoryDependency = Annotated[
    ScrapedProductDataRepository, Depends(ScrapedProductDataRepository)
]
