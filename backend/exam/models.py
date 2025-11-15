import uuid
from conf.database import Base
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import (
    Integer, String, DateTime, JSON, Text,
    ARRAY, UUID, func
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
if TYPE_CHECKING:
    from result.models import AttemptAnswer
    from result.models import ExamAttempt


class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    complexity: Mapped[str] = mapped_column(String)
    ques_type: Mapped[str] = mapped_column(String)

    options: Mapped[dict] = mapped_column(JSON)
    correct_answers: Mapped[dict] = mapped_column(JSON)

    max_score: Mapped[int] = mapped_column(Integer)
    tags: Mapped[List[str]] = mapped_column(ARRAY(String))

    # Relationships
    attempt_answers: Mapped[List["AttemptAnswer"]
                            ] = relationship(back_populates="question")

    def __repr__(self):
        return f"<Question(title={self.title}, complexity={self.complexity})>"


class Exam(Base):
    __tablename__ = 'exams'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now())
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(
        String, default="Draft")

    questions_order: Mapped[List[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)))

    # Relationships
    attempts: Mapped[List["ExamAttempt"]] = relationship(back_populates="exam")

    def __repr__(self):
        return f"<Exam(title={self.title}, status={self.status})>"
