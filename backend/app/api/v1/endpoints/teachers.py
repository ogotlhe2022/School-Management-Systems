from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.teacher import Teacher as TeacherModel
from app.schemas.teacher import Teacher, TeacherCreate, TeacherUpdate

router = APIRouter()


@router.get("/", response_model=List[Teacher])
async def list_teachers(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(TeacherModel).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{teacher_id}", response_model=Teacher)
async def get_teacher(teacher_id: int, session: AsyncSession = Depends(get_session)):
    teacher = await session.get(TeacherModel, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


@router.post("/", response_model=Teacher, status_code=status.HTTP_201_CREATED)
async def create_teacher(body: TeacherCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.execute(select(TeacherModel).where(TeacherModel.email == body.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    teacher = TeacherModel(**body.model_dump())
    session.add(teacher)
    await session.commit()
    await session.refresh(teacher)
    return teacher


@router.put("/{teacher_id}", response_model=Teacher)
async def update_teacher(teacher_id: int, body: TeacherUpdate, session: AsyncSession = Depends(get_session)):
    teacher = await session.get(TeacherModel, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(teacher, field, value)
    await session.commit()
    await session.refresh(teacher)
    return teacher


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(teacher_id: int, session: AsyncSession = Depends(get_session)):
    teacher = await session.get(TeacherModel, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    await session.delete(teacher)
    await session.commit()
    return None
