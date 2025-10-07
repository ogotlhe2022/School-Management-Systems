from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.student import Student as StudentModel
from app.schemas.student import Student, StudentCreate, StudentUpdate

router = APIRouter()


@router.get("/", response_model=List[Student])
async def list_students(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(StudentModel).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)):
    student = await session.get(StudentModel, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(body: StudentCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.execute(select(StudentModel).where(StudentModel.email == body.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    student = StudentModel(**body.model_dump())
    session.add(student)
    await session.commit()
    await session.refresh(student)
    return student


@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: int, body: StudentUpdate, session: AsyncSession = Depends(get_session)):
    student = await session.get(StudentModel, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
    await session.commit()
    await session.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, session: AsyncSession = Depends(get_session)):
    student = await session.get(StudentModel, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    await session.delete(student)
    await session.commit()
    return None
