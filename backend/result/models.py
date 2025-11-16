import uuid
from conf.database import Base
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import (
    Integer, DateTime, Boolean, ForeignKey, JSON, UUID, func
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
if TYPE_CHECKING:
    from auth.models import User
    from exam.models import Exam, Question


class ExamAttempt(Base):
    __tablename__ = 'exam_attempts'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('exams.id'))

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now())
    end_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True))
    is_submitted: Mapped[bool] = mapped_column(Boolean, default=False)
    total_score: Mapped[Optional[float]] = mapped_column(Integer, default=None)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="attempts")
    exam: Mapped["Exam"] = relationship("Exam", back_populates="attempts")
    attempt_answers: Mapped[List["AttemptAnswer"]] = relationship(
        "AttemptAnswer",
        back_populates="attempt"
    )

    def __repr__(self):
        return f"<ExamAttempt(user_id={self.user_id}, exam_id={self.exam_id}, submitted={self.is_submitted})>"


class AttemptAnswer(Base):
    __tablename__ = 'attempt_answers'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    attempt_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('exam_attempts.id'))
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('questions.id'))

    student_answer: Mapped[dict] = mapped_column(JSON)
    score: Mapped[Optional[float]] = mapped_column(Integer, default=None)
    is_graded: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    attempt: Mapped["ExamAttempt"] = relationship("ExamAttempt", back_populates="attempt_answers")
    question: Mapped["Question"] = relationship("Question", back_populates="attempt_answers")

    def __repr__(self):
        return f"<AttemptAnswer(attempt_id={self.attempt_id}, question_id={self.question_id})>"

