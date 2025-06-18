from typing import Annotated, List, Optional
from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from db import SessionContext
from models.product import Product


class ProductRepository:
    def __init__(self, session: SessionContext):
        self.session = session

    async def get_products(self) -> List[Product]:
        query = select(Product)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Optional[Product]:
        query = select(Product).where(Product.id == id)
        result = await self.session.execute(query)
        return result.scalar()

    async def create_product(
        self, global_query_name: str, description: Optional[str] = None
    ) -> Product:
        query = (
            insert(Product)
            .values(global_query_name=global_query_name, description=description)
            .returning(Product)
        )
        result = await self.session.execute(query)
        product = result.scalar()
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update_product(
        self, id: int, global_query_name: str, description: Optional[str] = None
    ) -> Product:
        product = await self.get_by_id(id)
        if not product:
            raise ValueError(f"Product with id {id} not found")

        query = (
            update(Product)
            .where(Product.id == id)
            .values(global_query_name=global_query_name, description=description)
            .returning(Product)
        )
        result = await self.session.execute(query)
        product = result.scalar()
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_product(self, id: int) -> Product:
        product = await self.get_by_id(id)
        if not product:
            raise ValueError(f"Product with id {id} not found")

        query = delete(Product).where(Product.id == id).returning(Product)
        await self.session.execute(query)
        await self.session.commit()
        return product


ProductRepositoryDependency = Annotated[ProductRepository, Depends(ProductRepository)]
