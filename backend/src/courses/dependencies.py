

from courses.repository import CoursesRepository
from courses.service import CoursesService


async def get_courses_service() -> CoursesService:
    repository = CoursesRepository()
    return CoursesService(repository)