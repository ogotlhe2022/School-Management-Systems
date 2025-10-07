from fastapi import APIRouter
from app.api.v1.endpoints import students, teachers, courses, sections, enrollments, attendance, grades

api_router = APIRouter()

api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(sections.router, prefix="/sections", tags=["sections"])
api_router.include_router(enrollments.router, prefix="/enrollments", tags=["enrollments"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(grades.router, prefix="/grades", tags=["grades"])
