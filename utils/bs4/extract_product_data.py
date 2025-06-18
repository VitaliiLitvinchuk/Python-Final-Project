from bs4 import BeautifulSoup
import re
from decimal import Decimal

from models.scraped_product_data import ScrapedProductData


async def extract_product_data(
    html, url: str, selectors: dict, product_id: int, platform_id: int, position: int
) -> ScrapedProductData:
    soup = BeautifulSoup(html, "html.parser")

    def get_text(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    def get_int(selector):
        text = get_text(selector)
        if not text:
            return 0
        match = re.search(r"\d+", text.replace(" ", "").replace(" ", ""))
        return int(match.group(0)) if match else 0

    def get_decimal(selector):
        el = soup.select_one(selector)
        if not el:
            return Decimal("0.00")

        text_parts = list(el.stripped_strings)
        full_text = "".join(text_parts)

        cleaned = re.sub(r"[^\d.,]", "", full_text).replace(",", ".")

        match = re.search(r"\d+(\.\d+)?", cleaned)
        return Decimal(match.group(0)) if match else Decimal("0.00")

    def get_rating(rating_selector):
        if isinstance(rating_selector, str):
            el = soup.select_one(rating_selector)
            if not el:
                return 0.0

            text = el.get_text(strip=True).replace(",", ".")
            match = re.search(r"\d+(\.\d+)?", text)
            return float(match.group(0)) if match else 0.0

        elif isinstance(rating_selector, dict):
            el = soup.select_one(rating_selector["selector"])
            if not el:
                return 0.0

            attr_value = el.get(rating_selector["percent_attribute"], "")
            percent_match = re.search(r"(\d+(?:\.\d+)?)%", attr_value)  # type: ignore
            if percent_match:
                percent = float(percent_match.group(1))
                return round((percent / 100) * 5, 2)
        return 0.0

    return ScrapedProductData(
        product_id=product_id,
        platform_id=platform_id,
        url_on_platform=url,
        name_on_platform=get_text(selectors["title_selector"]) or "",
        price=get_decimal(selectors["price_selector"]),
        currency=get_text(selectors["currency_selector"]) or "UAH",
        rating=get_rating(selectors["rating_selector"]),
        reviews_count=get_int(selectors["reviews_count_selector"]),
        availability_status=get_text(selectors["availability_selector"]) or "Невідомо",
        search_position=position,
    )
