from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class SectionBase(BaseModel):
    name: str
    room: Optional[str] = None
    course_id: int


class SectionCreate(SectionBase):
    pass


class SectionUpdate(BaseModel):
    name: Optional[str] = None
    room: Optional[str] = None
    course_id: Optional[int] = None


class Section(SectionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
