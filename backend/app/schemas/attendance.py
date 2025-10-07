from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class AttendanceBase(BaseModel):
    student_id: int
    section_id: int
    date: date
    status: str


class AttendanceCreate(AttendanceBase):
    pass


class Attendance(AttendanceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
