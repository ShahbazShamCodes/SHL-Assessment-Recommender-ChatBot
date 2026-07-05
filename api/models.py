from typing import List
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class Recommendation(BaseModel):
    entity_id: str
    name: str
    url: str
    duration: str
    assessment_type: str
    job_levels: str
    languages: str
    remote: str
    adaptive: str


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    answer: str
    recommendations: List[Recommendation]


    