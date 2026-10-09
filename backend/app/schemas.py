from pydantic import BaseModel, Field
from typing import List, Optional

class MCQQuestion(BaseModel):
    question: str
    options: List[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str
    explanation: str

class SubjectiveQuestion(BaseModel):
    question: str
    grading_rubric: str
    example_ideal_answer: str

class GuardrailEvaluation(BaseModel):
    is_topic_relevant: bool
    rejection_reason: Optional[str] = None

class MockTestPayload(BaseModel):
    guardrail: GuardrailEvaluation
    topic: str
    mcq_questions: List[MCQQuestion] = []
    subjective_questions: List[SubjectiveQuestion] = []

class GenerateTestRequest(BaseModel):
    doc_id: str
    topic_prompt: str
    chat_history: List[dict] = []
