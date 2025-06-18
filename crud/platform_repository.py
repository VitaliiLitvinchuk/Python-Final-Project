from typing import Annotated, List, Optional
from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from db import SessionContext
from models.platform import Platform


class PlatformRepository:
    def __init__(self, session: SessionContext):
        self.session = session

    async def get_platforms(self) -> List[Platform]:
        query = select(Platform)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Optional[Platform]:
        query = select(Platform).where(Platform.id == id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_by_name(self, name: str) -> Optional[Platform]:
        query = select(Platform).where(Platform.name == name)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_platforms_by_ids(self, ids: List[int]) -> List[Platform]:
        query = select(Platform).where(Platform.id.in_(ids))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_all_platforms_ids(self) -> List[int]:
        query = select(Platform.id)
        result = await self.session.execute(query)
        return [x[0] for x in result.all()]

    async def create_platform(
        self, name: str, base_url: str, search_url_template: Optional[str] = None
    ) -> Platform:
        if await self.get_by_name(name):
            raise ValueError(f"Platform with name {name} already exists")

        query = (
            insert(Platform)
            .values(
                name=name, base_url=base_url, search_url_template=search_url_template
            )
            .returning(Platform)
        )
        result = await self.session.execute(query)
        platform = result.scalar()
        await self.session.commit()
        await self.session.refresh(platform)
        return platform

    async def update_platform(
        self,
        id: int,
        name: str,
        base_url: str,
        search_url_template: Optional[str] = None,
    ) -> Platform:
        platform = await self.get_by_name(name)
        if platform and platform.id != id:
            raise ValueError(f"Platform with name {name} already exists")

        platform = await self.get_by_id(id)
        if not platform:
            raise ValueError(f"Platform with id {id} not found")

        query = (
            update(Platform)
            .where(Platform.id == id)
            .values(
                name=name, base_url=base_url, search_url_template=search_url_template
            )
            .returning(Platform)
        )
        result = await self.session.execute(query)
        platform = result.scalar()
        await self.session.commit()
        await self.session.refresh(platform)
        return platform

    async def delete_platform(self, id: int) -> Platform:
        platform = await self.get_by_id(id)
        if not platform:
            raise ValueError(f"Platform with id {id} not found")

        query = delete(Platform).where(Platform.id == id).returning(Platform)
        await self.session.execute(query)
        await self.session.commit()
        return platform


PlatformRepositoryDependency = Annotated[
    PlatformRepository, Depends(PlatformRepository)
]
