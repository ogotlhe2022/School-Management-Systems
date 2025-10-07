from __future__ import annotations

from datetime import date
from sqlalchemy import Integer, ForeignKey, Date, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, TimestampMixin


class Attendance(TimestampMixin, Base):
    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint("student_id", "section_id", "date", name="uq_attendance_unique"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id", ondelete="CASCADE"), index=True)
    section_id: Mapped[int] = mapped_column(Integer, ForeignKey("sections.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="present")  # present/absent

    student = relationship("Student", back_populates="attendances")
    section = relationship("Section", back_populates="attendances")
