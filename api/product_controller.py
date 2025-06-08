from fastapi import APIRouter
from crud.product_repository import ProductRepositoryDependency
from schemas.product_schema import ProductSchema

product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.post("", summary="Create new product")
async def create_product(
    product_repository: ProductRepositoryDependency,
    product: ProductSchema,
):
    return await product_repository.create_product(**product.dict())


@product_router.get("", summary="Get all products")
async def get_products(
    product_repository: ProductRepositoryDependency,
):
    return await product_repository.get_products()


@product_router.get("/{product_id}", summary="Get product by id")
async def get_product_by_id(
    product_repository: ProductRepositoryDependency,
    product_id: int,
):
    return await product_repository.get_by_id(product_id)


@product_router.put("/{product_id}", summary="Update product by id")
async def update_product_by_id(
    product_repository: ProductRepositoryDependency,
    product_id: int,
    product: ProductSchema,
):
    return await product_repository.update_product(product_id, **product.dict())


@product_router.delete("/{product_id}", summary="Delete product by id")
async def delete_product_by_id(
    product_repository: ProductRepositoryDependency,
    product_id: int,
):
    return await product_repository.delete_product(product_id)
