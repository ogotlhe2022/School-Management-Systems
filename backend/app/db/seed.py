import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.db.init_db import init_db
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.course import Course
from app.models.section import Section
from app.models.enrollment import Enrollment


async def seed() -> None:
    # Ensure tables exist
    await init_db()
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        # teachers
        t1 = Teacher(first_name="Ada", last_name="Lovelace", email="ada@example.com")
        t2 = Teacher(first_name="Alan", last_name="Turing", email="alan@example.com")
        session.add_all([t1, t2])
        await session.flush()

        # courses
        c1 = Course(name="Computer Science 101", code="CS101", teacher_id=t1.id)
        c2 = Course(name="Discrete Mathematics", code="MATH201", teacher_id=t2.id)
        session.add_all([c1, c2])
        await session.flush()

        # sections
        s1 = Section(name="CS101 - A", room="R1", course_id=c1.id)
        s2 = Section(name="MATH201 - B", room="R2", course_id=c2.id)
        session.add_all([s1, s2])
        await session.flush()

        # students
        st1 = Student(first_name="Grace", last_name="Hopper", email="grace@example.com")
        st2 = Student(first_name="Katherine", last_name="Johnson", email="katherine@example.com")
        session.add_all([st1, st2])
        await session.flush()

        # enroll
        e1 = Enrollment(student_id=st1.id, section_id=s1.id)
        e2 = Enrollment(student_id=st2.id, section_id=s2.id)
        session.add_all([e1, e2])

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
