# Import models here so that Base.metadata.create_all sees them
from app.db.base_class import Base  # noqa: F401
# isort: off
from app.models.student import Student  # noqa: F401
from app.models.teacher import Teacher  # noqa: F401
from app.models.course import Course  # noqa: F401
from app.models.section import Section  # noqa: F401
from app.models.enrollment import Enrollment  # noqa: F401
from app.models.attendance import Attendance  # noqa: F401
from app.models.grade import Grade  # noqa: F401
# isort: on
