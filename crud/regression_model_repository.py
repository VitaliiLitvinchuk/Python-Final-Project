from typing import Annotated, List, Optional, Dict
from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from db import SessionContext
from models.regression_model import RegressionModel


class RegressionModelRepository:
    def __init__(self, session: SessionContext):
        self.session = session

    async def get_regression_models(self) -> List[RegressionModel]:
        query = select(RegressionModel)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Optional[RegressionModel]:
        query = select(RegressionModel).where(RegressionModel.id == id)
        result = await self.session.execute(query)
        return result.scalar()

    async def create_regression_model(
        self,
        name: str,
        target_variable: str,
        feature_variables: List[str],
        coefficients_json: Dict[str, float],
        intercept: Optional[float] = None,
        r_squared: Optional[float] = None,
        platform_id: Optional[int] = None,
    ) -> RegressionModel:
        query = (
            insert(RegressionModel)
            .values(
                name=name,
                target_variable=target_variable,
                feature_variables=feature_variables,
                coefficients_json=coefficients_json,
                intercept=intercept,
                r_squared=r_squared,
                platform_id=platform_id,
            )
            .returning(RegressionModel)
        )
        result = await self.session.execute(query)
        regression_model = result.scalar()
        await self.session.commit()
        await self.session.refresh(regression_model)
        return regression_model

    async def update_regression_model(
        self,
        id: int,
        name: str,
        target_variable: str,
        feature_variables: List[str],
        coefficients_json: Dict[str, float],
        intercept: Optional[float] = None,
        r_squared: Optional[float] = None,
        platform_id: Optional[int] = None,
    ) -> RegressionModel:
        regression_model = await self.get_by_id(id)
        if not regression_model:
            raise ValueError(f"RegressionModel with id {id} not found")

        query = (
            update(RegressionModel)
            .where(RegressionModel.id == id)
            .values(
                name=name,
                target_variable=target_variable,
                feature_variables=feature_variables,
                coefficients_json=coefficients_json,
                intercept=intercept,
                r_squared=r_squared,
                platform_id=platform_id,
            )
            .returning(RegressionModel)
        )
        result = await self.session.execute(query)
        regression_model = result.scalar()
        await self.session.commit()
        await self.session.refresh(regression_model)
        return regression_model

    async def delete_regression_model(self, id: int) -> RegressionModel:
        regression_model = await self.get_by_id(id)
        if not regression_model:
            raise ValueError(f"RegressionModel with id {id} not found")

        query = (
            delete(RegressionModel)
            .where(RegressionModel.id == id)
            .returning(RegressionModel)
        )
        await self.session.execute(query)
        await self.session.commit()
        return regression_model


RegressionModelRepositoryDependency = Annotated[
    RegressionModelRepository, Depends(RegressionModelRepository)
]
