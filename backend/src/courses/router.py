from typing import List
from fastapi import APIRouter, Depends, HTTPException

from courses.repository import CoursesRepository
from courses.service import CoursesService
from schemas import CalendarSection, Course, CourseInfo, Message, Schedule, Semester, Subject
from courses.dependencies import get_courses_service

service = CoursesService(CoursesRepository())

def courses_router() -> APIRouter:
    router = APIRouter(prefix="", tags=["Courses"])

    @router.get("/semesters", response_model=List[Semester])
    async def get_semesters():
        try:
            return await service.list_semesters()
        
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to get semesters.")
        
    
    @router.get("/subjects/{semester_code}", response_model=List[Subject])
    async def get_subjects(
        semester_code: str,
    ):
        try:
            return await service.list_subjects(semester_code)
        
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to get subjects.")
        
    
    @router.patch("/addcourse", response_model=Message)
    async def add_given_course(
        course_info: CourseInfo,
    ):
        # try:
        return await service.add_course(course_info.semester_code, course_info.subject_code, course_info.course_code)
        
        # except Exception:
        #     raise HTTPException(status_code=500, detail="Failed to get course sections.")
        
    
    @router.get("/allcourses", response_model=List[Course])
    async def get_all_courses():
        try:
            return await service.list_all_courses()
        
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to get all courses.")
        

    @router.patch("/schedules", response_model=Message)
    async def generate_possible_schedules():
        # try:
        return await service.generate_possible_schedules()
        # except Exception:
        #     raise HTTPException(status_code=500, detail="Failed to generate schedules.")
        
    @router.get("/schedules", response_model=List[Schedule])
    async def get_schedules():
        #try: 
        return await service.get_schedules()
        # except Exception:
        #     raise HTTPException(status_code=500, detail="Failed to get schedules.")
    
    return router

