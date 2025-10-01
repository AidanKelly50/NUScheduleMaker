
import api from '@/hooks/api';
import type { Semester, Subject } from '@/types';

/**
 * Fetch semesters from the API.
 * @returns A list of Semester.
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