from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
from fastapi.middleware.cors import CORSMiddleware
from agents.resource_agent import find_study_resources
from agents.quiz_agent import create_quiz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # For development. Lock this down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Pydantic models -----

class LearnRequest(BaseModel):
    topic: str

class LearnResponse(BaseModel):
    topics: Dict[str, str]

class QuizRequest(BaseModel):
    subtopics: List[str]

class QuizQuestion(BaseModel):
    question: str
    option1: str
    option2: str
    option3: str
    option4: str
    answer: int
    topic: str
    explanation: str

class QuizResponse(BaseModel):
    questions: List[QuizQuestion]

# ----- Endpoints -----

@app.post("/learn", response_model=LearnResponse)
async def learn(request: LearnRequest):
    """
    Given a broad topic, returns subtopics and resources as a JSON mapping.
    """
    return find_study_resources(request.topic)

@app.post("/quiz", response_model=QuizResponse)
async def quiz(request: QuizRequest):
    """
    Given subtopics, returns a list of quiz questions (with options and explanations).
    """
    return create_quiz(request.subtopics)
