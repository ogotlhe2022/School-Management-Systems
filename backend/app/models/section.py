from __future__ import annotations

from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, TimestampMixin


class Section(TimestampMixin, Base):
    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    room: Mapped[str | None] = mapped_column(String(50), nullable=True)

    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    course: Mapped["Course"] = relationship("Course", back_populates="sections")

    enrollments: Mapped[List["Enrollment"]] = relationship("Enrollment", back_populates="section", cascade="all, delete-orphan")
    attendances: Mapped[List["Attendance"]] = relationship("Attendance", back_populates="section", cascade="all, delete-orphan")
    grades: Mapped[List["Grade"]] = relationship("Grade", back_populates="section", cascade="all, delete-orphan")
