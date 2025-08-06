from typing import ClassVar
from langchain.tools import BaseTool
from tavily import TavilyClient
from config import settings

class TavilySearchTool(BaseTool):
    name: ClassVar[str] = "tavily_search"
    description: ClassVar[str] = (
        "Useful for searching beginner-friendly educational articles or videos with concise queries (max 400 chars)."
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    def _run(self, query: str) -> str:
        query = query.strip()
        if len(query) > 400:
            query = query[:400]
        print(f"[TavilySearchTool] Query (truncated if needed): {query}")
        results = self._client.search(query=query, max_results=5)
        if not results or "results" not in results:
            return "No results found."
        for res in results["results"]:
            url = res.get("url", "")
            if "youtube.com" in url:
                return f"{res.get('title', '')} - {url}"
        top = results["results"][0]
        return f"{top.get('title', '')} - {top.get('url', '')}"

    async def _arun(self, query: str) -> str:
        return self._run(query)
