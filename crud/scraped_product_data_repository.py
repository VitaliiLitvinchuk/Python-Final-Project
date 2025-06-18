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

    async def get_by_product_id(self, product_id: int) -> List[ScrapedProductData]:
        query = select(ScrapedProductData).where(
            ScrapedProductData.product_id == product_id
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_platform_id(self, platform_id: int) -> List[ScrapedProductData]:
        query = select(ScrapedProductData).where(
            ScrapedProductData.platform_id == platform_id
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_platform_id_product_id(
        self, platform_id: int, product_id: int
    ) -> List[ScrapedProductData]:
        query = select(ScrapedProductData).where(
            ScrapedProductData.platform_id == platform_id,
            ScrapedProductData.product_id == product_id,
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

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

    async def bulk_create_scraped_product_data(
        self, data: List
    ) -> List[ScrapedProductData]:
        values = [
            {
                "product_id": int(item.product_id),
                "platform_id": int(item.platform_id),
                "url_on_platform": item.url_on_platform,
                "name_on_platform": item.name_on_platform,
                "price": Decimal(str(item.price)),
                "currency": item.currency,
                "rating": float(item.rating),
                "reviews_count": int(item.reviews_count),
                "availability_status": item.availability_status,
                "search_position": int(item.search_position),
            }
            for item in data
        ]
        query = insert(ScrapedProductData).values(values).returning(ScrapedProductData)
        result = await self.session.execute(query)
        await self.session.commit()
        return list(result.scalars().all())

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
