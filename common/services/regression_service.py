from typing import Annotated
from fastapi import Depends
import statsmodels.api as sm
import pandas as pd
from crud.regression_model_repository import RegressionModelRepositoryDependency
from crud.scraped_product_data_repository import ScrapedProductDataRepositoryDependency
from models.regression_model import RegressionModel


class RegressionAnalysisService:
    def __init__(
        self,
        regression_model_repository: RegressionModelRepositoryDependency,
        scraped_product_data_repository: ScrapedProductDataRepositoryDependency,
    ):
        self.regression_model_repository = regression_model_repository
        self.scraped_product_data_repository = scraped_product_data_repository

    async def train_regression_model(
        self, platform_id: int, product_id: int
    ) -> RegressionModel:
        result = (
            await self.scraped_product_data_repository.get_by_platform_id_product_id(
                platform_id,
                product_id,
            )
        )
        if not result:
            raise ValueError("No data available for regression.")

        df = pd.DataFrame(
            [
                {
                    "price": float(row.price),
                    "rating": float(row.rating),
                    "reviews_count": int(row.reviews_count),
                    "search_position": int(row.search_position),
                }
                for row in result
            ]
        )

        X = df[["price", "rating", "reviews_count"]]
        X = sm.add_constant(X)

        y = df["search_position"]

        model = sm.OLS(y, X).fit()

        intercept = model.params["const"]
        coefficients = {key: val for key, val in model.params.items() if key != "const"}
        r_squared = model.rsquared

        regression_model = RegressionModel(
            name=f"Regression for platform {platform_id}",
            target_variable="search_position",
            feature_variables=list(coefficients.keys()),
            coefficients_json=coefficients,
            intercept=intercept,
            r_squared=r_squared,
            platform_id=platform_id,
        )

        result = await self.regression_model_repository.create_regression_model(
            **regression_model.dict_model()
        )

        return result


RegressionAnalysisServiceDependency = Annotated[
    RegressionAnalysisService, Depends(RegressionAnalysisService)
]
