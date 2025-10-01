

import requests


class CoursesRepository:
    def __init__(self):
        self.cur_semester = ""
        self.all_classes_all_sections = []

        # self.breaks_list = [Break("0830", "1100", [True, False, True, False, False])]

    def get_semesters(self):
        sems_url = "https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?offset=1&max=15"
        semesters = requests.get(sems_url)
        return semesters
    
    def get_subjects(self, semester_code):
        url = f"https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/get_subject?&term={semester_code}&offset=1&max=300"
        subjects = requests.get(url)
        return subjects