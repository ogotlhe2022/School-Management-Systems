from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.models.section import Section as SectionModel
from app.schemas.section import Section, SectionCreate, SectionUpdate

router = APIRouter()


@router.get("/", response_model=List[Section])
async def list_sections(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SectionModel).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{section_id}", response_model=Section)
async def get_section(section_id: int, session: AsyncSession = Depends(get_session)):
    section = await session.get(SectionModel, section_id)
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    return section


@router.post("/", response_model=Section, status_code=status.HTTP_201_CREATED)
async def create_section(body: SectionCreate, session: AsyncSession = Depends(get_session)):
    section = SectionModel(**body.model_dump())
    session.add(section)
    await session.commit()
    await session.refresh(section)
    return section


@router.put("/{section_id}", response_model=Section)
async def update_section(section_id: int, body: SectionUpdate, session: AsyncSession = Depends(get_session)):
    section = await session.get(SectionModel, section_id)
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(section, field, value)
    await session.commit()
    await session.refresh(section)
    return section


@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(section_id: int, session: AsyncSession = Depends(get_session)):
    section = await session.get(SectionModel, section_id)
    if not section:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    await session.delete(section)
    await session.commit()
    return None
