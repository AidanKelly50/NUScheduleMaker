from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class BaseAPIModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

class CourseInfo(BaseAPIModel):
    semester_code: Optional[str] = None
    subject_code: str
    course_code: str

class Semester(BaseAPIModel):
    code: str
    description: str

class Subject(BaseAPIModel):
    code: str
    description: str

class MeetingTime(BaseAPIModel):
    building_description: Optional[str] = None
    begin_time: Optional[str] = None
    end_time: Optional[str] = None
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool

class Section(BaseAPIModel):
    course_reference_number: str
    sequence_number: str
    campus_description: str
    maximum_enrollment: int
    seats_available: int
    credit_hour_low: int
    faculty: List[str]
    instructional_method: str
    meeting_times: List[MeetingTime]

class CalendarSection(Section):
    subject: str
    course_number: str
    color_code: int

class Course(BaseAPIModel):
    subject: str
    course_number: str
    course_title: str
    sections: List[Section]
    color_code: int

class Schedule(BaseAPIModel):
    sections: List[CalendarSection]


class Message(BaseAPIModel):
    text: str