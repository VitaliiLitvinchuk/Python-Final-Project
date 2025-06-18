from fastapi import APIRouter

from common.services.scrape_service import ScrapeServiceDependency
from schemas.scrape_schema import ScrapeSchema


scrape_router = APIRouter(
    prefix="/scrape",
    tags=["Scrape"],
)


@scrape_router.post("/")
async def scrape(scrape_service: ScrapeServiceDependency, scrape: ScrapeSchema):
    return await scrape_service.scrape(scrape.product_id, scrape.platforms_ids)
