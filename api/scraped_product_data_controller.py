from fastapi import APIRouter
from crud.scraped_product_data_repository import ScrapedProductDataRepositoryDependency
from schemas.scraped_product_data_schema import ScrapedProductDataSchema

scraped_product_data_router = APIRouter(
    prefix="/scraped-product-data", tags=["scraped product data"]
)


@scraped_product_data_router.post("", summary="Create new scraped product data")
async def create_scraped_product_data(
    scraped_product_data_repository: ScrapedProductDataRepositoryDependency,
    scraped_product_data: ScrapedProductDataSchema,
):
    return await scraped_product_data_repository.create_scraped_product_data(
        **scraped_product_data.dict()
    )


@scraped_product_data_router.get("", summary="Get all scraped product data")
async def get_scraped_product_data(
    scraped_product_data_repository: ScrapedProductDataRepositoryDependency,
):
    return await scraped_product_data_repository.get_scraped_product_data()


@scraped_product_data_router.get("/{data_id}", summary="Get scraped product data by id")
async def get_scraped_product_data_by_id(
    scraped_product_data_repository: ScrapedProductDataRepositoryDependency,
    data_id: int,
):
    return await scraped_product_data_repository.get_by_id(data_id)


@scraped_product_data_router.get(
    "/product/{product_id}", summary="Get all scraped product data by product id"
)
async def get_scraped_product_data_by_product_id(
    scraped_product_data_repository: ScrapedProductDataRepositoryDependency,
    product_id: int,
):
    return await scraped_product_data_repository.get_by_product_id(product_id)


@scraped_product_data_router.get(
    "/platform/{platform_id}", summary="Get all scraped product data by platform id"
)
async def get_scraped_product_data_by_platform_id(
    scraped_product_data_repository: ScrapedProductDataRepositoryDependency,
    platform_id: int,
):
    return await scraped_product_data_repository.get_by_platform_id(platform_id)


@scraped_product_data_router.put(
    "/{data_id}", summary="Update scraped product data by id"
)
async def update_scraped_product_data_by_id(
    scraped_product_data_repository: ScrapedProductDataRepositoryDependency,
    data_id: int,
    scraped_product_data: ScrapedProductDataSchema,
):
    return await scraped_product_data_repository.update_scraped_product_data(
        data_id, **scraped_product_data.dict()
    )


@scraped_product_data_router.delete(
    "/{data_id}", summary="Delete scraped product data by id"
)
async def delete_scraped_product_data_by_id(
    scraped_product_data_repository: ScrapedProductDataRepositoryDependency,
    data_id: int,
):
    return await scraped_product_data_repository.delete_scraped_product_data(data_id)
