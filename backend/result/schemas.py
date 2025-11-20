import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class IDBase(BaseModel):
    id: uuid.UUID

class AttemptAnswerBase(BaseModel):
    question_id: uuid.UUID
    student_answer: Dict[str, Any]

class AttemptAnswerOut(AttemptAnswerBase, IDBase):
    score: Optional[float]
    is_graded: bool

    class Config:
        from_attributes = True

class ExamAttemptStart(BaseModel):
    exam_id: uuid.UUID

class ExamAttemptProgress(BaseModel):
    answers: List[AttemptAnswerBase]

class ExamAttemptOut(IDBase):
    user_id: uuid.UUID
    exam_id: uuid.UUID
    start_time: datetime
    end_time: Optional[datetime]
    is_submitted: bool
    total_score: Optional[float]
    attempt_answers: List[AttemptAnswerOut]

    class Config:
        from_attributes = True

class ResultSummaryOut(BaseModel):
    attempt_id: uuid.UUID
    exam_title: str
    user_email: str
    is_submitted: bool
    total_score: Optional[float]
    graded_count: int
    total_questions: int

    class Config:
        from_attributes = True
