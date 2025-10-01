

from backend.src.courses.repository import CoursesRepository
from backend.src.courses.service import CoursesService


async def get_courses_service() -> CoursesService:
    repository = CoursesRepository()
    return CoursesService(repository)