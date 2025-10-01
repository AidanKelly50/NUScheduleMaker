from typing import List
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException

from backend.src.courses.service import CoursesService
from backend.src.schemas import Semester, Subject
from backend.src.courses.dependencies import get_courses_service

def courses_router() -> APIRouter:
    router = APIRouter(prefix="", tags=["Courses"])

    @router.get("/semesters", response_model=List[Semester])
    async def get_semesters(service: CoursesService = Depends(get_courses_service)):
        try:
            return await service.list_semesters()
        
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to get semesters.")
        
    
    @router.get("/subjects/{semesterCode}", response_model=List[Subject])
    async def get_subjects(
        semesterCode: str,
        service: CoursesService = Depends(get_courses_service)
    ):
        try:
            return await service.list_subjects(semesterCode)
        
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to get subjects.")
        
    return router