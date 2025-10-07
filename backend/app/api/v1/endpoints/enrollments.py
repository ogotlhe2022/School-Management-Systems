from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.enrollment import Enrollment as EnrollmentModel
from app.schemas.enrollment import Enrollment, EnrollmentCreate

router = APIRouter()


@router.get("/", response_model=List[Enrollment])
async def list_enrollments(skip: int = 0, limit: int = 200, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(EnrollmentModel).offset(skip).limit(limit))
    return result.scalars().all()


@router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
async def create_enrollment(body: EnrollmentCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.execute(
        select(EnrollmentModel).where(
            (EnrollmentModel.student_id == body.student_id)
            & (EnrollmentModel.section_id == body.section_id)
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already enrolled")
    enrollment = EnrollmentModel(**body.model_dump())
    session.add(enrollment)
    await session.commit()
    await session.refresh(enrollment)
    return enrollment


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(enrollment_id: int, session: AsyncSession = Depends(get_session)):
    enrollment = await session.get(EnrollmentModel, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    await session.delete(enrollment)
    await session.commit()
    return None
