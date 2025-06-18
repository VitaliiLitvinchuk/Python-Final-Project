from typing import List
from pydantic import BaseModel


class ScrapeSchema(BaseModel):
    product_id: int = 1
    platforms_ids: List[int] = []
