import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .models import ExamStatus

class IDBase(BaseModel):
    id: uuid.UUID


class QuestionBase(BaseModel):
    title: str
    complexity: str
    ques_type: str
    options: Dict[str, Any]
    correct_answers: Dict[str, Any]
    max_score: int
    tags: List[str]


class QuestionCreate(QuestionBase):
    pass


class QuestionFilter(BaseModel):
    search_term: Optional[str] = None
    complexity: Optional[str] = None
    ques_type: Optional[str] = None
    tags: Optional[List[str]] = None

class QuestionOut(QuestionBase, IDBase):
    class Config:
        from_attributes = True
        

class QuestionImportSummary(BaseModel):
    total_rows_parsed: int
    new_questions_created: int
    import_successful: bool
    errors: List[str] = Field(default_factory=list)

class ExamCreate(BaseModel):
    title: str = Field(..., max_length=255)
    start_time: datetime
    end_time: datetime
    duration_minutes: int = Field(..., gt=0)
    question_ids: List[uuid.UUID]

class ExamUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[ExamStatus] = None
    question_ids: Optional[List[uuid.UUID]] = None

class ExamOut(IDBase):
    title: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    status: ExamStatus
    questions_order: List[uuid.UUID]

    class Config:
        from_attributes = True

