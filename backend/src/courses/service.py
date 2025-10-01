

from backend.src.courses.repository import CoursesRepository
from backend.src.schemas import Semester, Subject


class CoursesService:

    def __init__(self, repository: CoursesRepository):
        self.repository = repository

    async def list_semesters(self):
        raw_data = self.repository.get_semesters().json()
        semesters = [Semester(**item) for item in raw_data]
        
        return semesters
    
    async def list_subjects(self, sem):
        raw_data = self.repository.get_subjects(sem).json()
        semesters = [Subject(**item) for item in raw_data]
        
        return semesters

        