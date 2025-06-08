from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(platform_router)
app.include_router(product_router)
app.include_router(regression_model_router)
app.include_router(scraped_product_data_router)


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")
