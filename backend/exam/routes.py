import uuid
from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from conf.database import get_db
from .services import ExamService
from auth.models import User
from auth.dependencies import get_current_user, get_admin_user
from .schemas import ExamCreate, ExamUpdate, ExamOut, QuestionImportSummary, QuestionFilter, QuestionOut, QuestionCreate


exam_router = APIRouter(prefix="/exam", tags=["Exams"])
exam_service = ExamService()


@exam_router.post("/import-excel", response_model=QuestionImportSummary)
async def import_questions(
    file: UploadFile = File(...,
                            description="Excel file (.xlsx) containing question data"),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Upload Excel file, preview (conceptual), and confirm import of questions 
    into the Question Bank. The file parsing step remains synchronous within the service.
    """
    return await exam_service.import_questions_from_excel(db, file)


@exam_router.get("/all-questions", response_model=List[QuestionOut])
async def list_and_filter_questions(
    filters: QuestionFilter = Depends(),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: List, filter, and search questions in the bank.
    Filters are passed as query parameters.
    """
    return await exam_service.list_questions(db, filters)


@exam_router.get("/view-question/{question_id}", response_model=QuestionOut)
async def view_single_question(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: View a single question with its options and correct answer(s).
    """
    return await exam_service.get_question_by_id(db, question_id)


@exam_router.post("/create-question", response_model=QuestionOut, status_code=status.HTTP_201_CREATED)
async def create_single_question(
    question_data: QuestionCreate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Admin: Manually create a single question (alternative to import)."""
    return await exam_service.create_question(db, question_data)


@exam_router.post("/create-exam", response_model=ExamOut, status_code=status.HTTP_201_CREATED)
async def create_exam(
    exam_data: ExamCreate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Admin: Create an exam by selecting questions and setting parameters."""
    return await exam_service.create_exam(db, exam_data)


@exam_router.patch("/update-exam/{exam_id}", response_model=ExamOut)
async def update_exam(
    exam_id: uuid.UUID,
    update_data: ExamUpdate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Admin: Update exam details, including publishing/unpublishing (via status update)."""
    return await exam_service.update_exam(db, exam_id, update_data)


@exam_router.get("/available-exam", response_model=List[ExamOut])
async def view_available_exams(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Student: View and start available exams (Published and within time window)."""
    return await exam_service.get_available_exams(db)
