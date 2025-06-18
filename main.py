from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from scalar_fastapi.scalar_fastapi import Layout

from api.scrape_controller import scrape_router
from api.platform_controller import platform_router
from api.product_controller import product_router
from api.regression_model_controller import regression_model_router
from api.scraped_product_data_controller import scraped_product_data_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scrape_router)
app.include_router(platform_router)
app.include_router(product_router)
app.include_router(regression_model_router)
app.include_router(scraped_product_data_router)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    if app.openapi_url:
        scalar = get_scalar_api_reference(
            openapi_url=app.openapi_url,
            title=app.title,
            layout=Layout.CLASSIC,
            default_open_all_tags=False,
        )

        return scalar
    else:
        return RedirectResponse(url="/docs")


@app.get("/")
def read_root():
    return RedirectResponse(url="/scalar")
