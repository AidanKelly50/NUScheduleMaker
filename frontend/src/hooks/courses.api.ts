
import api from '@/hooks/api';
import type { Course, Message, Schedule, Semester, Subject } from '@/types';

/**
 * Fetch semesters from the API.
 * @returns A list of Semesters.
 */
export const getSemesters = async () => {
  const { data }: { data: Semester[] } = await api.get('/semesters');
  return data;
};

/**
 * Fetch subjects from the API.
 * @returns A list of Subjects.
 */
export const getSubjects = async (semester: string) => {
  const { data }: { data: Subject[] } = await api.get(`/subjects/${semester}`);
  return data;
};

/**
 * Add a course in the API.
 * @param semesterCode The code of the semester of the course to add
 * @param subjectCode The code of the subject of the course to add
 * @param courseCode The code of the course to add
 * @returns Success message
 */
export const addCourse = async (
    { semesterCode, subjectCode, courseCode }: 
    { semesterCode: string, subjectCode: string, courseCode: string }
) => {
  const { data }: { data: Message } = await api.patch('/addcourse', {
    semesterCode: semesterCode,
    subjectCode: subjectCode,
    courseCode: courseCode
  });
  return data;
};


/**
 * Fetch semesters from the API.
 * @returns A list of Semesters.
 */
export const getCourses = async () => {
  const { data }: { data: Course[] } = await api.get('/allcourses');
  return data;
};

/**
 * Fetch newly generated schedules from the API.
 * @returns A list of Schedules.
 */
export const generateSchedules = async () => {
  const { data }: { data: Message } = await api.patch('/schedules');
  return data;
};

/**
 * Fetch schedules from the API.
 * @returns A list of Schedules.
 */
export const getSchedules = async () => {
  const { data }: { data: Schedule[] } = await api.get('/schedules');
  return data;
};