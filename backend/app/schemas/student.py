from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class Student(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
