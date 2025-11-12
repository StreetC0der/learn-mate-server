import os
import re
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langchain_groq import ChatGroq  # Groq LangChain integration

def extract_json_array(text: str) -> list:
    """
    Extract JSON array from LLM output that might contain extra text or formatting.
    """
    # Remove any markdown or code fences first
    cleaned = re.sub(r"``````", "", text, flags=re.DOTALL | re.IGNORECASE).strip()

    # Extract the JSON array part
    match = re.search(r"\[.*\]", cleaned, re.DOTALL)
    if match:
        return json.loads(match.group())
    else:
        raise ValueError("No valid JSON array found in response.")

def create_quiz(subtopics: list) -> dict:
    """
    Generate quiz questions for the given list of subtopics.
    Returns dict with "questions": List[dict].
    """
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")

    # Instantiate Groq LLM with your API key
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",  # Use 8b model for faster, cheaper quiz generation; switch to bigger model if needed
        api_key=GROQ_API_KEY,
        temperature=0
    )

    prompt_template = """
You are a quiz generator for beginner learners. For each of the subtopics in the list below, create ONE multiple-choice question with 4 answer options.
Specify the correct option number (1-4) and provide a 1-2 sentence explanation for the correct answer.

Return ONLY a JSON array of objects in the exact format below, and no other text:

[
  {{
    "question": "Your question here?",
    "option1": "Answer option 1",
    "option2": "Answer option 2",
    "option3": "Answer option 3",
    "option4": "Answer option 4",
    "answer": 2,
    "topic": "Corresponding subtopic",
    "explanation": "Short explanation why this answer is correct"
  }},
  ...
]

Subtopics: {subtopics}
"""

    prompt = prompt_template.format(subtopics=json.dumps(subtopics))

    print("[create_quiz] Sending prompt to LLM:")
    print(prompt)

    # Call the model and get raw string
    response = llm.invoke(prompt).content

    print("[create_quiz] Raw LLM output:")
    print(response)

    try:
        questions = extract_json_array(response)
    except Exception as e:
        print(f"Failed to parse quiz questions JSON: {e}")
        questions = []

    return {"questions": questions}
