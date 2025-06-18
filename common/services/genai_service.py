from typing import Annotated
from anyio import sleep
from fastapi import Depends, HTTPException
from common.app_settings import AppSettingsDependency
from google import genai
from playwright.async_api import async_playwright


class GenaiService:
    def __init__(self, settings: AppSettingsDependency):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def analyze_page(self, url: str, return_prompt: str) -> str:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=60_000)
                await page.wait_for_load_state("networkidle")
                await sleep(10)

                html_content = await page.content()
                await browser.close()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Помилка при завантаженні сторінки з Playwright: {str(e)}",
            )

        prompt = f"""
        Потрібно проаналізувати сторінку та виконати умови нижче.
        
        {return_prompt}
        
        Дані:
        {html_content}
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=[prompt],
                # model="gemini-2.0-flash-live-001",
                # contents=[prompt],
            )
            response_text = response.text
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Помилка при виклику Gemini API: {str(e)}"
            )

        if not response_text:
            raise HTTPException(status_code=400, detail="Помилка при аналізі сторінки")

        return response_text.strip()


GenaiServiceDependency = Annotated[GenaiService, Depends(GenaiService)]
