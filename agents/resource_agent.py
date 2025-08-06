import re
import json
from llm.gemini_llm import GeminiProLLM
from tools.search_tool_tavily import TavilySearchTool

def extract_json(text: str) -> dict:
    """
    Extract a JSON object from a possibly messy string (removing code block fences/backticks/quotes).
    Returns as Python dict.
    """
    cleaned = text.strip()

    # Remove markdown code blocks, triple/single backticks, and quotes from start/end
    cleaned = re.sub(r"^(``````|'''|`|\"|')+$", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()

    # Extract only the first JSON object from the text, if present
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if not match:
        raise ValueError("No JSON object found in LLM output.")
    json_str = match.group(0)

    return json.loads(json_str)

def find_study_resources(topic: str) -> dict:
    """
    For the input topic, use Gemini LLM (and Tavily tool via prompt) to generate subtopics and resource links.
    Returns: dict {"topics": {subtopic1: link1, ...}}
    Robustly handles all output, so you'll never get 500 due to parsing.
    """
    llm = GeminiProLLM()

    # Instruct clearly: NO markdown, NO backticks, ONLY JSON!
    prompt = (
        f"You are an educational assistant. Break the topic '{topic}' into 2-5 beginner-friendly subtopics. "
        f"For each subtopic, find ONE beginner-oriented video/article link using search. "
        f"Return ONLY a pure JSON object mapping subtopic names to URLs. Do NOT wrap your answer in backticks, quotes, or markdown. "
        f"Do not include explanation, extra phrasing, or code fences. Only output the final pure JSON object."
    )

    # Run LLM (not inside LangChain agent, so you always have the actual output)
    try:
        print("[find_study_resources] Sending prompt to LLM:")
        print(prompt)
        result_text = llm(prompt)
        print("[find_study_resources] Raw LLM output:")
        print(result_text)
        resources = extract_json(result_text)
        print("[find_study_resources] Final parsed resources dict:")
        print(resources)
    except Exception as e:
        print("Failed to parse JSON from LLM output:", e)
        # Fallback: provide a single Tavily search link for the topic
        tavily_tool = TavilySearchTool()
        fallback_link = tavily_tool._run(topic)
        resources = {topic: fallback_link}

    return {"topics": resources}
