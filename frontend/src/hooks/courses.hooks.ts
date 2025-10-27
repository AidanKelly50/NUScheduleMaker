import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { getSemesters, getSubjects, addCourse, getCourses, generateSchedules, getSchedules } from '@/hooks/courses.api';

/**
 * A react-query hook to fetch all of the semesters.
 * @returns A react-query hook to fetch semesters.
 */
export const useSemesters = () => {
    return useQuery({
        queryKey: ['semesters'],
        queryFn: () => getSemesters()
    });
};


/**
 * A react-query hook to fetch all of the subjects.
 * @returns A react-query hook to fetch subjects.
 */
export const useSubjects = (semester: string) => {
    return useQuery({
        queryKey: ['subjects', semester],
        queryFn: () => getSubjects(semester),
        enabled: !!semester
    });
};

/**
 * A react-query mutation hook to add a course to the course list, including a toast notification
 * @returns A react-query mutation hook to add a course, including a toast notification
 */
export const useAddCourse = () => {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: addCourse,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['courses']
      });
    }
  });

  const mutate = async (
    { semesterCode, subjectCode, courseCode }: 
    { semesterCode: string, subjectCode: string, courseCode: string }) =>
    toast.promise(mutation.mutateAsync({ semesterCode, subjectCode, courseCode }), {
      loading: 'Adding course...',
      success: () => ({
        message: 'Course added successfully.',
        description: `${subjectCode} ${courseCode}`
      }),
      error: 'An error occurred while adding the course.'
    });
  return { ...mutation, mutate };
};

/**
 * A react-query hook to fetch all of the courses and sections.
 * @returns A react-query hook to fetch courses.
 */
export const useCourses = () => {
    return useQuery({
        queryKey: ['courses'],
        queryFn: () => getCourses()
    });
};

/**
 * A react-query mutation hook to generate all possible schedules, including a toast notification
 * @returns A react-query mutation hook to generate schedules, including a toast notification
 */
export const useGenerateSchedules = () => {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: generateSchedules,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['schedules']
      });
    }
  });

  const mutate = async () =>
    toast.promise(mutation.mutateAsync(), {
      loading: 'Generating schedules...',
      success: () => ({
        message: 'Schedules generated successfully.',
        description: 'Generates schedules.'
      }),
      error: 'An error occurred while generating schedules.'
    });
  return { ...mutation, mutate };
};

/**
 * A react-query hook to fetch all of the possible schedules.
 * @returns A react-query hook to fetch schedules.
 */
export const useSchedules = () => {
    return useQuery({
        queryKey: ['schedules'],
        queryFn: () => getSchedules()
    });
};