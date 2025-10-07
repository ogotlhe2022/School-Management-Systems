from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EnrollmentBase(BaseModel):
    student_id: int
    section_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class Enrollment(EnrollmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
