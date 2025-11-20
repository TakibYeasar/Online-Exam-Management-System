import uuid
from typing import List, Any
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from conf.database import get_db
from .services import ExamService
from auth.models import UserRole
from .schemas import ExamCreate, ExamUpdate, ExamOut, QuestionImportSummary, QuestionFilter, QuestionOut, QuestionCreate


exam_router = APIRouter()
exam_service = ExamService()


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


@exam_router.post("/import-excel", response_model=QuestionImportSummary)
def import_questions(
    file: UploadFile = File(...,
                            description="Excel file (.xlsx) containing question data"),
    db: Session = Depends(get_db),
    admin: Any = Depends(get_admin_user)
):
    """
    Admin: Upload Excel file, preview (conceptual), and confirm import of questions 
    into the Question Bank.
    """
    return exam_service.import_questions_from_excel(db, file)


@exam_router.get("/", response_model=List[QuestionOut])
def list_and_filter_questions(
    filters: QuestionFilter = Depends(),
    db: Session = Depends(get_db),
    admin: Any = Depends(get_admin_user)
):
    """
    Admin: List, filter, and search questions in the bank.
    Filters are passed as query parameters (e.g., /questions?ques_type=text&search_term=gravity).
    """
    return exam_service.list_questions(db, filters)


@exam_router.get("/{question_id}", response_model=QuestionOut)
def view_single_question(
    question_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: Any = Depends(get_admin_user)
):
    """
    Admin: View a single question with its options and correct answer(s).
    """
    return exam_service.get_question_by_id(db, question_id)


@exam_router.post("/", response_model=QuestionOut, status_code=status.HTTP_201_CREATED)
def create_single_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    admin: Any = Depends(get_admin_user)
):
    """
    Admin: Manually create a single question (alternative to import).
    """
    return exam_service.import_questions_from_excel(db, [question_data.model_dump()]).newly_created_questions[0]

@exam_router.post("/", response_model=ExamOut, status_code=status.HTTP_201_CREATED)
def create_exam(
    exam_data: ExamCreate,
    db: Session = Depends(get_db),
    admin: MockUser = Depends(get_admin_user)
):
    """Admin: Create an exam by selecting questions and setting parameters."""
    return exam_service.create_exam(db, exam_data)


@exam_router.patch("/{exam_id}", response_model=ExamOut)
def update_exam(
    exam_id: uuid.UUID,
    update_data: ExamUpdate,
    db: Session = Depends(get_db),
    admin: MockUser = Depends(get_admin_user)
):
    """Admin: Update exam details, including publishing/unpublishing (via status update)."""
    return exam_service.update_exam(db, exam_id, update_data)

@exam_router.get("/available", response_model=List[ExamOut])
def view_available_exams(
    db: Session = Depends(get_db),
    user: MockUser = Depends(get_current_user)
):
    """Student: View and start available exams (Published and within time window)."""
    return exam_service.get_available_exams(db)
