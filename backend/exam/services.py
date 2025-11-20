import uuid
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from fastapi import HTTPException, status, UploadFile
from .models import Exam, Question, ExamStatus
from .schemas import ExamCreate, ExamUpdate, QuestionBase, QuestionFilter, QuestionImportSummary


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
            # Placeholder data simulating successful parsing of 2 rows
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
    def import_questions_from_excel(self, db: Session, file: UploadFile) -> QuestionImportSummary:
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
            db.commit()
            return QuestionImportSummary(
                total_rows_parsed=len(parsed_data),
                new_questions_created=new_questions_created,
                import_successful=True,
                errors=errors
            )
        except Exception as e:
            db.rollback()
            errors.append(f"Database commit failed: {e}")
            return QuestionImportSummary(
                total_rows_parsed=len(parsed_data),
                new_questions_created=0,
                import_successful=False,
                errors=errors
            )

    # Admin: List, Filter, and Search Questions
    def list_questions(self, db: Session, filters: QuestionFilter) -> List[Question]:
        query = db.query(Question)

        if filters.ques_type:
            query = query.filter(Question.ques_type == filters.ques_type)

        if filters.complexity:
            query = query.filter(Question.complexity == filters.complexity)

        if filters.tags:
            for tag in filters.tags:
                query = query.filter(Question.tags.contains([tag]))

        if filters.search_term:
            search = f"%{filters.search_term}%"
            query = query.filter(
                or_(
                    Question.title.ilike(search),
                    Question.complexity.ilike(search)
                )
            )

        return query.all()

    # Admin: Get Single Question
    def get_question_by_id(self, db: Session, question_id: uuid.UUID) -> Question:
        question = db.query(Question).filter(
            Question.id == question_id).first()
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")
        return question
    
    # Admin: Create Exam
    def create_exam(self, db: Session, exam_data: ExamCreate) -> Exam:
        if exam_data.start_time >= exam_data.end_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Start time must be before end time.")

        questions = db.query(Question).filter(
            Question.id.in_(exam_data.question_ids)).all()
        if len(questions) != len(exam_data.question_ids):
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
        db.commit()
        db.refresh(new_exam)
        return new_exam
    
    # Admin: Update Exam (including publish/unpublish)
    def update_exam(self, db: Session, exam_id: uuid.UUID, update_data: ExamUpdate) -> Exam:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found.")

        update_dict = update_data.model_dump(exclude_unset=True)

        if 'question_ids' in update_dict:
            questions = db.query(Question).filter(
                Question.id.in_(update_dict['question_ids'])).all()
            if len(questions) != len(update_dict['question_ids']):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="One or more question IDs are invalid.")
            update_dict['questions_order'] = update_dict.pop('question_ids')

        for key, value in update_dict.items():
            setattr(exam, key, value)

        db.add(exam)
        db.commit()
        db.refresh(exam)
        return exam
    
    # Student: View Available Exams
    def get_available_exams(self, db: Session) -> List[Exam]:
        now = func.now()
        exams = db.query(Exam).filter(
            Exam.status == ExamStatus.PUBLISHED,
            Exam.start_time <= now,
            Exam.end_time >= now
        ).all()
        return exams

    # Get a single Exam by ID
    def get_exam_by_id(self, db: Session, exam_id: uuid.UUID) -> Exam:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found.")
        return exam

