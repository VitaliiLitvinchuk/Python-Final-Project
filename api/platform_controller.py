from fastapi import APIRouter
from crud.platform_repository import PlatformRepositoryDependency
from schemas.platfrom_schema import PlatformSchema

platform_router = APIRouter(prefix="/platforms", tags=["platforms"])


@platform_router.post("", summary="Create new platform")
async def create_platform(
    platform_repository: PlatformRepositoryDependency,
    platform: PlatformSchema,
):
    platform_data = platform.dict()
    platform_data["base_url"] = str(platform_data["base_url"])
    platform_data["search_url_template"] = str(platform_data["search_url_template"])
    return await platform_repository.create_platform(**platform_data)


@platform_router.get("", summary="Get all platforms")
async def get_platforms(
    platform_repository: PlatformRepositoryDependency,
):
    return await platform_repository.get_platforms()


@platform_router.get("/search/{platform_name}", summary="Get platform by name")
async def get_platform_by_name(
    platform_repository: PlatformRepositoryDependency,
    platform_name: str,
):
    return await platform_repository.get_by_name(platform_name)


@platform_router.get("/{platform_id}", summary="Get platform by id")
async def get_platform_by_id(
    platform_repository: PlatformRepositoryDependency,
    platform_id: int,
):
    return await platform_repository.get_by_id(platform_id)


@platform_router.put("/{platform_id}", summary="Update platform by id")
async def update_platform_by_id(
    platform_repository: PlatformRepositoryDependency,
    platform_id: int,
    platform: PlatformSchema,
):
    return await platform_repository.update_platform(platform_id, **platform.dict())


@platform_router.delete("/{platform_id}", summary="Delete platform by id")
async def delete_platform_by_id(
    platform_repository: PlatformRepositoryDependency,
    platform_id: int,
):
    return await platform_repository.delete_platform(platform_id)
