import { useQuery } from '@tanstack/react-query';
import { toast } from 'sonner';
import { getSemesters, getSubjects } from '@/hooks/courses.api';
import type { Semester } from '@/types';

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