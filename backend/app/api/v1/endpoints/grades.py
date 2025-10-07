from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.grade import Grade as GradeModel
from app.schemas.grade import Grade, GradeCreate

router = APIRouter()


@router.get("/", response_model=List[Grade])
async def list_grades(skip: int = 0, limit: int = 200, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(GradeModel).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=Grade, status_code=status.HTTP_201_CREATED)
async def create_grade(body: GradeCreate, session: AsyncSession = Depends(get_session)):
    grade = GradeModel(**body.model_dump())
    session.add(grade)
    await session.commit()
    await session.refresh(grade)
    return grade


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(grade_id: int, session: AsyncSession = Depends(get_session)):
    grade = await session.get(GradeModel, grade_id)
    if not grade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    await session.delete(grade)
    await session.commit()
    return None
