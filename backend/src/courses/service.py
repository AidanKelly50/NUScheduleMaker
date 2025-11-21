

from courses.repository import CoursesRepository
from schemas import CalendarSection, Course, MeetingTime, Message, Schedule, Section, Semester, Subject


class CoursesService:

    def __init__(self, repository: CoursesRepository):
        self.repository = repository
        self.used_color_codes = []

    async def list_semesters(self):
        raw_data = (await self.repository.get_semesters()).json()
        semesters = [Semester(**item) for item in raw_data]
        
        return semesters
    
    async def list_subjects(self, sem):
        raw_data = (await self.repository.get_subjects(sem)).json()
        subjects = [Subject(**item) for item in raw_data]
        
        return subjects

    async def add_course(self, semester_code, subject_code, course_code):
        await self.repository.add_course_to_list(semester_code, subject_code, course_code)
        return Message(text="Added course")
    
    def format_meetings(self, meetings_list):
        formatted_meetings = []
        for meeting in meetings_list:
            cur_meeting = MeetingTime(
                building_description=meeting["buildingDescription"],
                begin_time=meeting["beginTime"],
                end_time=meeting["endTime"],
                monday=meeting["monday"],
                tuesday=meeting["tuesday"],
                wednesday=meeting["wednesday"],
                thursday=meeting["thursday"],
                friday=meeting["friday"]
            )
            formatted_meetings.append(cur_meeting)

        return formatted_meetings
    
    async def list_all_courses(self):
        all_courses = await self.repository.get_all_courses()
        formatted_courses = []

        for course in all_courses:

            formatted_sections = []
            for section in course:
                formatted_meetings = self.format_meetings(section["meetingTimes"])
                    
                cur_section = Section(
                    course_reference_number=section["courseReferenceNumber"],
                    sequence_number=section["sequenceNumber"],
                    campus_description=section["campusDescription"],
                    maximum_enrollment=section["maximumEnrollment"],
                    seats_available=section["seatsAvailable"],
                    credit_hour_low=section["creditHourLow"],
                    faculty=section["faculty"],
                    instructional_method=section["instructionalMethod"],
                    meeting_times=formatted_meetings,
                )
                formatted_sections.append(cur_section)

            cur_course = Course(
                subject=course[0]["subject"], 
                course_number=course[0]["courseNumber"],
                course_title=course[0]["courseTitle"],
                sections=formatted_sections,
                color_code=(await self.repository.get_course_color(course[0]["subject"], course[0]["courseNumber"]))
            )
            formatted_courses.append(cur_course)

        return formatted_courses

    async def generate_possible_schedules(self):
        await self.repository.generate_schedules()
        return Message(text="Schedules Generated.")
    
    async def get_schedules(self):
        all_courses = await self.list_all_courses()
        all_schedules = await self.repository.get_possible_schedules()

        formatted_schedules = []

        for schedule in all_schedules:
            formatted_single_schedule = []

            for i in range(len(schedule)):
                formatted_meetings = self.format_meetings(schedule[i]["meetingTimes"])

                cur_section = CalendarSection(
                    course_reference_number=schedule[i]["courseReferenceNumber"],
                    sequence_number=schedule[i]["sequenceNumber"],
                    campus_description=schedule[i]["campusDescription"],
                    maximum_enrollment=schedule[i]["maximumEnrollment"],
                    seats_available=schedule[i]["seatsAvailable"],
                    credit_hour_low=schedule[i]["creditHourLow"],
                    faculty=schedule[i]["faculty"],
                    instructional_method=schedule[i]["instructionalMethod"],
                    meeting_times=formatted_meetings,
                    subject=all_courses[i].subject,
                    course_number=all_courses[i].course_number,
                    color_code=all_courses[i].color_code
                )
                formatted_single_schedule.append(cur_section)
            
            cur_schedule = Schedule(sections=formatted_single_schedule)
            formatted_schedules.append(cur_schedule)

        return formatted_schedules
    

