from langchain_core.language_models import BaseLanguageModel as LLM
import google.generativeai as genai
from config import settings

genai.configure(api_key=settings.gemini_api_key)


class GeminiProLLM(LLM):
    def _call(self, prompt: str, stop=None) -> str:
        # Change the model name here to "gemini-2.5-pro"
        response = genai.GenerativeModel("gemini-2.5-pro").generate_content(prompt)
        return response.text

    @property
    def _identifying_params(self):
        return {"name": "GeminiPro"}

    @property
    def _llm_type(self):
        return "gemini-pro"
