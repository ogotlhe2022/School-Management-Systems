from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class GradeBase(BaseModel):
    student_id: int
    section_id: int
    assignment: str
    score: int


class GradeCreate(GradeBase):
    pass


class Grade(GradeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
