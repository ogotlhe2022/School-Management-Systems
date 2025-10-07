from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class CourseBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    teacher_id: Optional[int] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    teacher_id: Optional[int] = None


class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
