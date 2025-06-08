from google import genai

from common.app_settings import settings

gemini_api_key = settings.GEMINI_API_KEY
client = genai.Client(api_key=gemini_api_key)
