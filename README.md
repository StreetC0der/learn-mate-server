# Agentic AI Backend

This is the backend part of the Agentic AI project — a FastAPI service that provides two primary endpoints to help learners:

- **/learn**: Breaks down a broad topic into beginner-friendly subtopics with curated resources.  
- **/quiz**: Generates quiz questions based on selected subtopics.

The backend integrates large language models (LLMs) and external search tools to deliver personalized educational content and quizzes.

## Table of Contents

- [Features](#features)  
- [Architecture](#architecture)  
- [Tech Stack](#tech-stack)  
- [Getting Started](#getting-started)  
- [Environment Variables](#environment-variables)  
- [API Endpoints](#api-endpoints)  
- [Folder Structure](#folder-structure)  
- [Troubleshooting](#troubleshooting)  
- [Contributing](#contributing)  
- [License](#license)

## Features

- **Topic Decomposition & Resource Curation**  
  Uses Google Gemini Pro (`gemini-2.5-pro`) LLM to break down topics into 2-10 subtopics with beginner-friendly resource links from Tavily search.

- **Quiz Generation**  
  Generates multiple-choice quiz questions per subtopic using Groq’s LLaMA 3 model via LangChain-Groq integration.

- **Robust Prompt Engineering & JSON Parsing**  
  Carefully constructed prompts and output parsing ensure consistent JSON responses without markdown/code block artifacts.

- **Secure API key management** with environment variables loaded via `.env`.

## Architecture

- **FastAPI** serves REST endpoints `/learn` and `/quiz`.
- **LLMs**:  
  - `GeminiProLLM` wraps Google Gemini for topic breakdown and resource discovery.  
  - `ChatGroq` wraps Groq’s LLaMA 3 for quiz question generation.
- **TavilySearchTool** integrates Tavily API for educational resource retrieval.
- **Configuration** handled via Pydantic `Settings` class from `.env`.

## Tech Stack

- Python 3.10+  
- FastAPI  
- Uvicorn (ASGI server)  
- LangChain (LLM orchestration)  
- Google Generative AI & Gemini LLM  
- Groq LLaMA 3 via LangChain-Groq  
- Tavily API  
- Pydantic for settings validation  
- python-dotenv for environment variables

## Getting Started

### Prerequisites

- Python 3.10 or higher  
- Access to Gemini and Groq API keys  
- Tavily API key  
- Git (optional)

### Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/agentic-ai-backend.git
   cd agentic-ai-backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv env
   source env/bin/activate    # Linux/macOS
   # or
   .\env\Scripts\activate     # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file in the project root with the following variables:

   ```
   TAVILY_API_KEY=your_tavily_api_key
   GEMINI_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

5. Run the API server:

   ```bash
   uvicorn api.main:app --reload
   ```

6. Access Swagger UI to test endpoints:

   ```
   http://127.0.0.1:8000/docs
   ```

## Environment Variables

Store API keys securely in `.env` file to avoid exposing them in code.

| Variable       | Description               |
| -------------- | ------------------------- |
| TAVILY_API_KEY | Tavily search API key     |
| GEMINI_API_KEY | Google Gemini LLM API key |
| GROQ_API_KEY   | Groq LLaMA 3 API key      |

## API Endpoints

### POST `/learn`

- **Request**:  
  JSON with a `topic` string.

  ```json
  {
    "topic": "Python Programming"
  }
  ```

- **Response**:  
  JSON mapping beginner-friendly subtopics to resource URLs.

  ```json
  {
    "topics": {
      "Python Basics": "https://example.com/python-basics",
      "Functions": "https://example.com/python-functions"
    }
  }
  ```

### POST `/quiz`

- **Request**:  
  JSON list of subtopics.

  ```json
  {
    "subtopics": ["Python Basics", "Functions"]
  }
  ```

- **Response**:  
  JSON list of multiple-choice quiz questions with options, answers, and explanations.

  ```json
  {
    "questions": [
      {
        "question": "What is a Python function?",
        "option1": "A loop",
        "option2": "A block of reusable code",
        "option3": "A variable type",
        "option4": "An operator",
        "answer": 2,
        "topic": "Functions",
        "explanation": "Functions in Python allow you to define reusable code blocks."
      }
    ]
  }
  ```

## Folder Structure

```
.
├── api/
│   └── main.py             # FastAPI app with route definitions
├── agents/
│   ├── resource_agent.py   # Topic breakdown & resource search logic
│   ├── quiz_agent.py       # Quiz question generation logic
├── llm/
│   └── gemini_llm.py       # GeminiProLLM wrapper
├── tools/
│   └── search_tool_tavily.py # Tavily search tool integration
├── config.py               # Pydantic settings class, loads .env
├── requirements.txt        # Dependencies
└── .env                   # API keys (not checked-in)
```

## Troubleshooting

- **LLM output parsing errors:**  
  Ensure your prompts request *only* raw JSON output, no markdown/code fences.

- **API key attribute errors:**  
  Pydantic maps `.env` keys to lowercase attributes (`GEMINI_API_KEY` → `settings.gemini_api_key`). Use lowercase in code.

- **Gemini LLM no output or fail on specific topics:**  
  Use fallback to Tavily results or handle empty resource gracefully.

- **500 errors:**  
  Check server logs for stack trace. Usually caused by JSON parsing or missing keys.

- **LangChain Deprecation Warnings:**  
  Update to current recommended LangChain usage before production if needed.

