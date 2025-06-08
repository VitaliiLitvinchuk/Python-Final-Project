from fastapi import APIRouter
from crud.regression_model_repository import RegressionModelRepositoryDependency
from schemas.regression_model_schema import RegressionModelSchema

regression_model_router = APIRouter(
    prefix="/regression-models", tags=["regression models"]
)


@regression_model_router.post("", summary="Create new regression model")
async def create_regression_model(
    regression_model_repository: RegressionModelRepositoryDependency,
    regression_model: RegressionModelSchema,
):
    return await regression_model_repository.create_regression_model(
        **regression_model.dict()
    )


@regression_model_router.get("", summary="Get all regression models")
async def get_regression_models(
    regression_model_repository: RegressionModelRepositoryDependency,
):
    return await regression_model_repository.get_regression_models()


@regression_model_router.get("/{model_id}", summary="Get regression model by id")
async def get_regression_model_by_id(
    regression_model_repository: RegressionModelRepositoryDependency,
    model_id: int,
):
    return await regression_model_repository.get_by_id(model_id)


@regression_model_router.put("/{model_id}", summary="Update regression model by id")
async def update_regression_model_by_id(
    regression_model_repository: RegressionModelRepositoryDependency,
    model_id: int,
    regression_model: RegressionModelSchema,
):
    return await regression_model_repository.update_regression_model(
        model_id, **regression_model.dict()
    )


@regression_model_router.delete("/{model_id}", summary="Delete regression model by id")
async def delete_regression_model_by_id(
    regression_model_repository: RegressionModelRepositoryDependency,
    model_id: int,
):
    return await regression_model_repository.delete_regression_model(model_id)
