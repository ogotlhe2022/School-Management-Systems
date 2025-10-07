from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.course import Course as CourseModel
from app.schemas.course import Course, CourseCreate, CourseUpdate

router = APIRouter()


@router.get("/", response_model=List[Course])
async def list_courses(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CourseModel).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{course_id}", response_model=Course)
async def get_course(course_id: int, session: AsyncSession = Depends(get_session)):
    course = await session.get(CourseModel, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
async def create_course(body: CourseCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.execute(select(CourseModel).where(CourseModel.code == body.code))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Code already exists")
    course = CourseModel(**body.model_dump())
    session.add(course)
    await session.commit()
    await session.refresh(course)
    return course


@router.put("/{course_id}", response_model=Course)
async def update_course(course_id: int, body: CourseUpdate, session: AsyncSession = Depends(get_session)):
    course = await session.get(CourseModel, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await session.commit()
    await session.refresh(course)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, session: AsyncSession = Depends(get_session)):
    course = await session.get(CourseModel, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    await session.delete(course)
    await session.commit()
    return None
