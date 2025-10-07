from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class Teacher(TeacherBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
