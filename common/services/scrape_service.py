from typing import Annotated, List

from fastapi import Depends, HTTPException

from common.services.genai_service import GenaiServiceDependency
from crud.platform_repository import PlatformRepositoryDependency
from crud.product_repository import ProductRepositoryDependency
from crud.scraped_product_data_repository import ScrapedProductDataRepositoryDependency
from models.scraped_product_data import ScrapedProductData
from utils.bs4.extract_product_data import extract_product_data
from utils.genai.normalize_json import normalize_json
from playwright.async_api import async_playwright


class ScrapeService:
    def __init__(
        self,
        platform_repository: PlatformRepositoryDependency,
        product_repository: ProductRepositoryDependency,
        scraped_product_data_repository: ScrapedProductDataRepositoryDependency,
        genai_service: GenaiServiceDependency,
    ):
        self.platform_repository = platform_repository
        self.product_repository = product_repository
        self.scraped_product_data_repository = scraped_product_data_repository
        self.genai_service = genai_service

    async def scrape(self, product_id: int, platforms_ids: List[int]):
        browser = None
        scraped_products: List[ScrapedProductData] = []
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-extensions",
                        "--proxy-server='direct://'",
                        "--proxy-bypass-list=*",
                        "--disable-gpu",
                        "--disable-dev-shm-usage",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-web-security",
                    ],
                )
                page = await browser.new_page()
                product = await self.product_repository.get_by_id(product_id)
                if product is None:
                    raise ValueError(f"Product with id {product_id} not found")
                search = product.global_query_name
                if len(platforms_ids) == 0:
                    platforms_ids = (
                        await self.platform_repository.get_all_platforms_ids()
                    )
                platforms = await self.platform_repository.get_platforms_by_ids(
                    platforms_ids
                )
                parsed = []
                for platform in platforms:
                    response = await self.genai_service.analyze_page(
                        platform.search_url_template.replace("{search}", search),  # type: ignore
                        """
                        Проаналізуй HTML-сторінку результатів пошуку та побудуй JSON-об’єкт у такому форматі:
                        {
                        "products": [
                            {
                            "link": "absolute URL to product page",
                            "search_position": 1
                            },
                            {
                            "link": "absolute URL to product page",
                            "search_position": 2
                            },
                            ...
                        ]
                        }
                        🔹 **link** — повне (абсолютне) посилання на сторінку продукту  
                        🔹 **search_position** — позиція продукту у результатах пошуку, починаючи з 1
                        ---
                        🎯 **Вимоги до вибірки**:
                        - Обробляй **лише головний блок із результатами пошуку** (наприклад, каталог товарів, грід або список товарів).
                        - Ігноруй банери, рекламу, рекомендовані товари, каруселі та інші другорядні блоки.
                        - Витягуй **тільки активні (видимі) продукти** — пропущені/приховані не враховувати.
                        - Не повинно бути `null` у полях (`link`, `search_position` мають бути присутні й валідні).
                        - Посилання повинні бути абсолютними (додавай `base_url`, якщо воно відсутнє у `href`).
                        ---
                        📌 Поверни **лише об'єкт JSON** без пояснень, коментарів або додаткового тексту.
                        """,
                    )
                    parsed_json = normalize_json(response)
                    parsed_json["platform_id"] = str(platform.id)
                    parsed.append(parsed_json)
                if len(parsed) == 0:
                    raise HTTPException(status_code=404, detail="No products found")
                for parse in parsed:
                    url = parse["products"][0]["link"]
                    raw_selectors = await self.genai_service.analyze_page(
                        url,
                        """
                        Надай стабільні CSS-селектори (класи, ID або вкладені атрибути) для використання з Playwright. Очікується об'єкт такого формату:
                        {
                        "title_selector": "CSS selector for product name",
                        "price_selector": "CSS selector for product price",
                        "currency_selector": "CSS selector for currency symbol",
                        "rating_selector": "Either a CSS selector for numeric rating OR an object { \"selector\": \"...\", \"percent_attribute\": \"...\" }",
                        "reviews_count_selector": "CSS selector for number of feedbacks/feedbacks and questions",
                        "availability_selector": "CSS selector for availability status"
                        "charecteristics": "CSS selector for button/link of expand characteristics"
                        }
                        🔹 **title_selector** — назва продукту
                        🔹 **price_selector** — ціна продукту
                        🔹 **currency_selector** — валюта (наприклад, "$", "₴", "€")
                        🔹 **rating_selector**:
                        - Якщо рейтинг вказано числом — поверни CSS селектор до цього числа.
                        - Якщо рейтинг реалізовано як відсоток (наприклад, через `style="width:80%"`) — поверни об'єкт:
                            {
                            "selector": "CSS селектор елемента",
                            "percent_attribute": "назва атрибута (наприклад, style)"
                            }
                        🔹 **reviews_count_selector** — кількість відгуків
                        🔹 **availability_selector** — текст про наявність (наприклад, "В наявності", "Очікується", "Немає")
                        🔹 **charecteristics** — CSS селектор кнопки/посилання відкриття характеристик
                        ---
                        🎯 **Вимоги**:
                        - Перевага надається **стабільним класам** або ID (без модифікаторів стану чи кольору).
                        - ❌ Не використовуй селектори з модифікаторами стану (наприклад, `green`, `red`, `disabled`)
                        - ❌ Не використовуй теги специфічних компонентів (наприклад, `<rz-stars-rating-progress>`) — лише класи або атрибути дочірніх HTML-елементів.
                        - 🔍 Селектори повинні бути **мінімальними, точними і придатними для Playwright**.
                        - Уникай занадто загальних або динамічних класів (типу `.ng-star-inserted`, `.active`, `.selected`).
                        Поверни **лише об’єкт JSON** без пояснень чи коментарів.
                        """,
                    )
                    selectors = normalize_json(raw_selectors)
                    for product in parse["products"]:
                        url = product["link"]
                        await page.goto(url, timeout=60_000)
                        await page.wait_for_load_state("networkidle")
                        scraped_data = await extract_product_data(
                            html=await page.content(),
                            url=url,
                            selectors=selectors,
                            product_id=product_id,
                            platform_id=int(parse["platform_id"]),
                            position=int(product["search_position"]),
                        )
                        # characteristics_data = {}
                        # try:
                        #     if (
                        #         "characteristics" in selectors
                        #         and selectors["characteristics"]
                        #     ):
                        #         await page.click(
                        #             selectors["characteristics"], timeout=1000
                        #         )
                        #         await page.wait_for_load_state("networkidle")
                        #         raw_characteristics_json = (
                        #             await self.genai_service.analyze_page(
                        #                 page.url,
                        #                 """
                        #             Проаналізуй HTML-сторінку та витягни всі доступні характеристики продукту, які представлені у форматі 'назва: значення'. Сформуй JSON-об’єкт у такому вигляді:
                        #             {
                        #             "characteristics": [
                        #                 {
                        #                 "name": "Назва характеристики 1",
                        #                 "value": "Значення характеристики 1"
                        #                 },
                        #                 {
                        #                 "name": "Назва характеристики 2",
                        #                 "value": "Значення характеристики 2"
                        #                 },
                        #                 ...
                        #             ]
                        #             }
                        #             🔹 **name** — це назва або етикетка характеристики (наприклад, 'Колір', 'Об'єм пам'яті', 'Тип матриці').
                        #             🔹 **value** — це відповідне значення характеристики (наприклад, 'Чорний', '256 ГБ', 'IPS').
                        #             ---
                        #             🎯 **Вимоги до вибірки**:
                        #             - Зосередься виключно на блоках, що містять перелік технічних характеристик, специфікацій або детальних параметрів продукту.
                        #             - Ігноруй будь-яку іншу інформацію: загальні описи продукту, рекламні блоки, відгуки, умови доставки, рекомендації тощо.
                        #             - Вибирай тільки **активні та видимі** характеристики.
                        #             - Переконайся, що кожна характеристика має як **назву**, так і **значення**, і що вони точно відповідають одна одній.
                        #             ---
                        #             📌 Поверни **ЛИШЕ ОБ'ЄКТ JSON** без будь-яких додаткових пояснень, коментарів чи іншого тексту. Збережи формат JSON валідним.
                        #             """,
                        #             )
                        #         )
                        #         characteristics_data = raw_characteristics_json
                        #         return characteristics_data
                        # except Exception as e:
                        #     print(
                        #         f"Не вдалося клікнути на характеристики або проаналізувати їх: {e}"
                        #     )
                        #     pass
                        # scraped_data.characteristics = characteristics_data.get(
                        #     "characteristics", []
                        # )
                        scraped_products.append(scraped_data)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Помилка при завантаженні сторінки з Playwright: {str(e)}",
            )
        finally:
            if browser is not None:
                await browser.close()

        return (
            await self.scraped_product_data_repository.bulk_create_scraped_product_data(
                scraped_products
            )
        )


ScrapeServiceDependency = Annotated[ScrapeService, Depends(ScrapeService)]
