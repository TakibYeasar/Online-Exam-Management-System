import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, or_
from sqlalchemy.future import select
from fastapi import HTTPException, status, UploadFile
from .models import Exam, Question, ExamStatus
from .schemas import ExamCreate, ExamUpdate, QuestionBase, QuestionFilter, QuestionImportSummary, QuestionCreate


class ExamService:
    
    def parse_excel_file(file: UploadFile) -> List[Dict[str, Any]]:
        """
        Conceptual function to read an XLSX file and return a list of question dictionaries.
        In a real application, this would use pandas/openpyxl and handle:
        - Reading the file into a DataFrame.
        - Renaming/Validating required columns (title, complexity, type, etc.).
        - Converting 'options' and 'correct_answers' (JSON string -> Dict).
        - Converting 'tags' (CSV string -> List).
        """
        if file.filename.endswith(".xlsx") or file.filename.endswith(".xls"):
            return [
                {
                    "title": "What is 2+2?",
                    "complexity": "Class 1",
                    "ques_type": "single_choice",
                    "options": {"A": "3", "B": "4", "C": "5"},
                    "correct_answers": {"selected_option": "B"},
                    "max_score": 5,
                    "tags": ["Math", "Basic"]
                },
                {
                    "title": "Describe gravity.",
                    "complexity": "Class 5",
                    "ques_type": "text",
                    "options": {},
                    "correct_answers": {"model_answer": "Gravity is the force that..."},
                    "max_score": 10,
                    "tags": ["Physics"]
                }
            ]
        else:
            raise ValueError("File must be an Excel (.xlsx) file.")
    
    # Helper function for grading objective questions
    def _grade_objective_question(self, question: Question, student_answer: Dict[str, Any]) -> float:
        correct_answers = question.correct_answers.get('selected_options', [])
        student_selected = student_answer.get('selected_options', [])

        if question.ques_type == 'single_choice':
            is_correct = set(student_selected) == set(correct_answers)
            return question.max_score if is_correct else 0.0

        elif question.ques_type == 'multiple_choice':
            if set(student_selected) == set(correct_answers):
                return question.max_score
            else:
                return 0.0

        return 0.0
    
    # Admin: Import Questions from Excel
    async def import_questions_from_excel(self, db: AsyncSession, file: UploadFile) -> QuestionImportSummary:
        errors = []
        parsed_data: List[Dict[str, Any]]

        try:
            parsed_data = self.parse_excel_file(file)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error parsing file: {e}")

        new_questions_created = 0

        for idx, row in enumerate(parsed_data):
            try:
                question_data = QuestionBase(**row)

                new_question = Question(
                    title=question_data.title,
                    complexity=question_data.complexity,
                    ques_type=question_data.ques_type,
                    options=question_data.options,
                    correct_answers=question_data.correct_answers,
                    max_score=question_data.max_score,
                    tags=question_data.tags
                )
                db.add(new_question)
                new_questions_created += 1

            except Exception as e:
                errors.append(
                    f"Row {idx + 1} ('{row.get('title', 'N/A')}'): Validation or DB error: {e}")

        try:
            await db.commit()
            return QuestionImportSummary(
                total_rows_parsed=len(parsed_data),
                new_questions_created=new_questions_created,
                import_successful=True,
                errors=errors
            )
        except Exception as e:
            await db.rollback()
            errors.append(f"Database commit failed: {e}")
            return QuestionImportSummary(
                total_rows_parsed=len(parsed_data),
                new_questions_created=0,
                import_successful=False,
                errors=errors
            )
    
    # Admin: Create Single Question (ADD THIS METHOD)
    async def create_question(self, db: AsyncSession, question_data: QuestionCreate) -> Question:
        """
        Manually creates a single Question record from the validated Pydantic model.
        """
        new_question = Question(**question_data.model_dump())

        db.add(new_question)

        await db.commit()
        await db.refresh(new_question)

        return new_question

    # Admin: List, Filter, and Search Questions
    async def list_questions(self, db: AsyncSession, filters: QuestionFilter) -> List[Question]:
        stmt = select(Question)

        if filters.ques_type:
            stmt = stmt.where(Question.ques_type == filters.ques_type)

        if filters.complexity:
            stmt = stmt.where(Question.complexity == filters.complexity)

        if filters.tags:
            for tag in filters.tags:
                stmt = stmt.where(Question.tags.contains([tag]))

        if filters.search_term:
            search = f"%{filters.search_term}%"
            stmt = stmt.where(
                or_(
                    Question.title.ilike(search),
                    Question.complexity.ilike(search)
                )
            )

        result = await db.execute(stmt)
        return result.scalars().all()

    # Admin: Get Single Question
    async def get_question_by_id(self, db: AsyncSession, question_id: uuid.UUID) -> Question:
        stmt = select(Question).where(Question.id == question_id)
        result = await db.execute(stmt)
        question = result.scalars().first()

        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")
        return question
    
    # Admin: Create Exam
    async def create_exam(self, db: AsyncSession, exam_data: ExamCreate) -> Exam:
        if exam_data.start_time >= exam_data.end_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Start time must be before end time.")

        question_id_count_stmt = select(func.count(Question.id)).where(
            Question.id.in_(exam_data.question_ids)
        )
        count_result = await db.execute(question_id_count_stmt)
        valid_question_count = count_result.scalar_one()

        if valid_question_count != len(exam_data.question_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="One or more question IDs are invalid.")

        new_exam = Exam(
            title=exam_data.title,
            start_time=exam_data.start_time,
            end_time=exam_data.end_time,
            duration_minutes=exam_data.duration_minutes,
            questions_order=exam_data.question_ids,
            status=ExamStatus.DRAFT
        )
        db.add(new_exam)
        await db.commit()
        await db.refresh(new_exam)
        return new_exam
    
    # Admin: Update Exam (including publish/unpublish)
    async def update_exam(self, db: AsyncSession, exam_id: uuid.UUID, update_data: ExamUpdate) -> Exam:
        stmt = select(Exam).where(Exam.id == exam_id)
        result = await db.execute(stmt)
        exam: Optional[Exam] = result.scalars().first()

        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found.")

        update_dict = update_data.model_dump(exclude_unset=True)

        if 'question_ids' in update_dict:
            question_id_count_stmt = select(func.count(Question.id)).where(
                Question.id.in_(update_dict['question_ids'])
            )
            count_result = await db.execute(question_id_count_stmt)
            valid_question_count = count_result.scalar_one()

            if valid_question_count != len(update_dict['question_ids']):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="One or more question IDs are invalid.")

            update_dict['questions_order'] = update_dict.pop('question_ids')

        for key, value in update_dict.items():
            setattr(exam, key, value)

        db.add(exam)
        await db.commit()
        await db.refresh(exam)
        return exam
    
    # Student: View Available Exams
    async def get_available_exams(self, db: AsyncSession) -> List[Exam]:
        now = func.now()

        stmt = (
            select(Exam)
            .where(
                Exam.status == ExamStatus.PUBLISHED,
                Exam.start_time <= now,
                Exam.end_time >= now
            )
        )

        result = await db.execute(stmt)
        exams = result.scalars().all()

        return exams

    # Get a single Exam by ID
    async def get_exam_by_id(self, db: AsyncSession, exam_id: uuid.UUID) -> Exam:
        stmt = select(Exam).where(Exam.id == exam_id)
        result = await db.execute(stmt)
        exam = result.scalars().first()

        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found.")
        return exam

