from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.attendance import Attendance as AttendanceModel
from app.schemas.attendance import Attendance, AttendanceCreate

router = APIRouter()


@router.get("/", response_model=List[Attendance])
async def list_attendance(skip: int = 0, limit: int = 200, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(AttendanceModel).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=Attendance, status_code=status.HTTP_201_CREATED)
async def create_attendance(body: AttendanceCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.execute(
        select(AttendanceModel).where(
            (AttendanceModel.student_id == body.student_id)
            & (AttendanceModel.section_id == body.section_id)
            & (AttendanceModel.date == body.date)
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Attendance already recorded")
    attendance = AttendanceModel(**body.model_dump())
    session.add(attendance)
    await session.commit()
    await session.refresh(attendance)
    return attendance


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(attendance_id: int, session: AsyncSession = Depends(get_session)):
    attendance = await session.get(AttendanceModel, attendance_id)
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
    await session.delete(attendance)
    await session.commit()
    return None
