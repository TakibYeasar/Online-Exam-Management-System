import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from conf.database import get_db
from pydantic import BaseModel, Field
from .services import ResultService
from .schemas import ExamAttemptStart, ExamAttemptOut, ExamAttemptProgress, AttemptAnswerOut, ResultSummaryOut
from auth.models import UserRole

result_router = APIRouter()
result_service = ResultService()


class MockUser(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str
    role: UserRole


def get_current_user():
    return MockUser(email="student@example.com", role=UserRole.STUDENT)


def get_admin_user(current_user: MockUser = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only Admins are allowed to perform this action.")
    return current_user


@result_router.post("/start", response_model=ExamAttemptOut)
def start_or_resume_attempt(
    attempt_data: ExamAttemptStart,
    db: Session = Depends(get_db),
    user: MockUser = Depends(get_current_user)
):
    """Student: Start a new exam attempt or resume an active one."""
    return result_service.start_exam_attempt(db, user.id, attempt_data.exam_id)


@result_router.post("/{attempt_id}/progress", response_model=List[AttemptAnswerOut])
def save_progress(
    attempt_id: uuid.UUID,
    progress_data: ExamAttemptProgress,
    db: Session = Depends(get_db),
    user: MockUser = Depends(get_current_user)
):
    """Student: Auto-save progress periodically/on change."""
    return result_service.save_attempt_progress(db, attempt_id, progress_data)


@result_router.post("/{attempt_id}/submit", response_model=ExamAttemptOut)
def submit_attempt(
    attempt_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: MockUser = Depends(get_current_user)
):
    """Student: Submit the exam, triggering auto-grading and total score calculation."""
    attempt = result_service.submit_exam_attempt(db, attempt_id)
    return attempt


@result_router.get("/{attempt_id}/summary", response_model=ResultSummaryOut)
def get_result_summary(
    attempt_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: MockUser = Depends(get_current_user)
):
    """Admin/Student: View the result summary (score, graded count)."""
    return result_service.get_result_summary(db, attempt_id)


@result_router.get("/{attempt_id}/full", response_model=ExamAttemptOut)
def get_full_result_details(
    attempt_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: MockUser = Depends(get_current_user)
):
    """Admin/Student: View the full result details, including all answers and scores."""
    return result_service.get_full_result(db, attempt_id)
