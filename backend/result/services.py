import uuid
from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from .models import ExamAttempt, AttemptAnswer
from .schemas import ExamAttemptProgress, ResultSummaryOut
from exam.services import ExamService
from exam.models import Exam, ExamStatus, Question


class ResultService:
    def __init__(self):
        self.exam_service = ExamService()

    # Student: Start Exam Attempt
    def start_exam_attempt(self, db: Session, user_id: uuid.UUID, exam_id: uuid.UUID) -> ExamAttempt:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam or exam.status != ExamStatus.PUBLISHED:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Exam not available.")

        active_attempt = db.query(ExamAttempt).filter(
            ExamAttempt.user_id == user_id,
            ExamAttempt.exam_id == exam_id,
            ExamAttempt.is_submitted == False
        ).first()

        if active_attempt:
            return active_attempt

        now = datetime.now(exam.start_time.tzinfo)
        if not (exam.start_time <= now and exam.end_time >= now):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Exam is outside the allowed time window.")

        new_attempt = ExamAttempt(
            user_id=user_id,
            exam_id=exam_id,
            start_time=func.now()
        )
        db.add(new_attempt)
        db.commit()
        db.refresh(new_attempt)
        return new_attempt

    # Student: Auto-save progress / Answer submission (Periodic save or on change)
    def save_attempt_progress(self, db: Session, attempt_id: uuid.UUID, progress_data: ExamAttemptProgress) -> List[AttemptAnswer]:
        attempt = db.query(ExamAttempt).filter(
            ExamAttempt.id == attempt_id, ExamAttempt.is_submitted == False).first()
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Active attempt not found.")

        saved_answers = []
        for answer_data in progress_data.answers:
            attempt_answer = db.query(AttemptAnswer).filter(
                AttemptAnswer.attempt_id == attempt_id,
                AttemptAnswer.question_id == answer_data.question_id
            ).first()

            if not attempt_answer:
                attempt_answer = AttemptAnswer(
                    attempt_id=attempt_id,
                    question_id=answer_data.question_id,
                    student_answer=answer_data.student_answer
                )
            else:
                attempt_answer.student_answer = answer_data.student_answer

            db.add(attempt_answer)
            saved_answers.append(attempt_answer)

        db.commit()
        return saved_answers

    # Student: Submit Exam
    def submit_exam_attempt(self, db: Session, attempt_id: uuid.UUID) -> ExamAttempt:
        attempt = db.query(ExamAttempt).filter(
            ExamAttempt.id == attempt_id, ExamAttempt.is_submitted == False).first()
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Active attempt not found.")

        attempt.is_submitted = True
        attempt.end_time = func.now()

        total_score = 0.0

        answers_to_grade = db.query(AttemptAnswer).filter(
            AttemptAnswer.attempt_id == attempt_id).all()
        question_ids = [ans.question_id for ans in answers_to_grade]
        questions = db.query(Question).filter(
            Question.id.in_(question_ids)).all()
        question_map = {q.id: q for q in questions}

        for answer in answers_to_grade:
            question = question_map.get(answer.question_id)
            if not question:
                continue

            if question.ques_type in ['single_choice', 'multiple_choice']:
                score = self.exam_service._grade_objective_question(
                    question, answer.student_answer)
                answer.score = score
                answer.is_graded = True
                total_score += score

            db.add(answer)

        attempt.total_score = total_score

        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt

    # Admin/Student: View Result Summary
    def get_result_summary(self, db: Session, attempt_id: uuid.UUID) -> ResultSummaryOut:
        attempt = db.query(ExamAttempt).filter(
            ExamAttempt.id == attempt_id).first()
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Exam attempt not found.")

        total_questions = len(
            attempt.exam.questions_order) if attempt.exam else 0
        graded_count = db.query(AttemptAnswer).filter(
            AttemptAnswer.attempt_id == attempt_id, AttemptAnswer.is_graded == True).count()

        summary = ResultSummaryOut(
            attempt_id=attempt.id,
            exam_title=attempt.exam.title,
            user_email=attempt.user.email,
            is_submitted=attempt.is_submitted,
            total_score=attempt.total_score,
            graded_count=graded_count,
            total_questions=total_questions
        )
        return summary

    # Admin/Student: View Full Result
    def get_full_result(self, db: Session, attempt_id: uuid.UUID) -> ExamAttempt:
        attempt = db.query(ExamAttempt).filter(
            ExamAttempt.id == attempt_id).first()
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Exam attempt not found.")
        return attempt

