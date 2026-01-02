import copy
import httpx
import pandas as pd
import utils.overlap_functions as overlap_functions

class CoursesRepository:
    def __init__(self):
        self.httpx_client = httpx.AsyncClient()
        self.all_courses = []
        self.course_colors = [] # [["CS", "3500", 0], ...]

        self.possible_schedules = []
        

        # self.breaks_list = [Break("0830", "1100", [True, False, True, False, False])]

    async def get_all_courses(self):
        return self.all_courses
    
    async def get_possible_schedules(self):
        return self.possible_schedules
    
    async def get_course_color(self, subject, course_code):
        for color in self.course_colors:
            if color[0] == subject and color[1] == course_code:
                return color[2]
            
        return self.course_colors[0][2]

    async def get_semesters(self):
        sems_url = "https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?offset=1&max=15"
        semesters = await self.httpx_client.get(sems_url)
        return semesters
    
    async def get_subjects(self, semester_code):
        url = f"https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/get_subject?&term={semester_code}&offset=1&max=300"
        subjects = await self.httpx_client.get(url)
        return subjects
    
    async def add_course(self, semester_code, subject_code, course_code):
        # SET TERM
        url = "https://nubanner.neu.edu/StudentRegistrationSsb/ssb/term/search"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",}
        data = {"term": semester_code,
                "studyPath": "",
                "studyPathText": "",
                "startDatepicker": "",
                "endDatepicker": ""}

        post_response = await self.httpx_client.post(url, headers=headers, data=data)
        if post_response.status_code != 200:
            print(f"Failed to declare term. Status code: {post_response.status_code}")
            print(post_response.text)
        # Get cookie data
        cookie_jar = post_response.cookies
        cookies_dict = dict(cookie_jar)

        # GET COURSE DATA
        base_url = "https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults"
        params = {"txt_subject": subject_code,
                "txt_courseNumber": course_code,
                "txt_term": semester_code,  # Use the term code previously declared
                "pageOffset": 0,
                "pageMaxSize": 100,
                "sortColumn": "subjectDescription",
                "sortDirection": "asc"}
        headers = {"Content-Type": "application/json"}

        # Make the GET request to retrieve course data
        class_response = await self.httpx_client.get(base_url, headers=headers, params=params, cookies=cookies_dict)
        if class_response.status_code != 200:
            print(f"Failed to retrieve course data. Status code: {class_response.status_code}")
            print(class_response.json())

        # BRING OUT MEETING INFO
        meeting_infos_list = []
        cr_json_data = class_response.json()["data"]

        for cur_section in cr_json_data:
            # Add professor into data
            faculty_names = await self.get_faculty_by_crn(semester_code, cur_section["courseReferenceNumber"])
            cur_section["faculty"] = faculty_names

            cur_section_meetings = []
            all_meetings_info = cur_section["meetingsFaculty"]
            

            for cur_meeting in all_meetings_info:
                cur_meeting_time_info = cur_meeting["meetingTime"]
                if cur_meeting_time_info["meetingType"] == "CLAS":
                    cur_meeting_dict = {"buildingDescription": cur_meeting_time_info["buildingDescription"],
                                        "beginTime": cur_meeting_time_info["beginTime"], 
                                        "endTime": cur_meeting_time_info["endTime"],
                                        "monday": cur_meeting_time_info["monday"],
                                        "tuesday": cur_meeting_time_info["tuesday"],
                                        "wednesday": cur_meeting_time_info["wednesday"],
                                        "thursday": cur_meeting_time_info["thursday"],
                                        "friday": cur_meeting_time_info["friday"]}
                
                    cur_section_meetings.append(cur_meeting_dict)

            meeting_infos_list.append(cur_section_meetings)

        # CREATE DF AND ADD METTING TIMES
        class_df = pd.DataFrame(cr_json_data)
        class_df.drop(["term", "termDesc", "partOfTerm", "subjectDescription", "linkIdentifier", "isSectionLinked", 
                        "instructionalMethodDescription", "meetingsFaculty", "reservedSeatSummary", "sectionAttributes", "crossListCapacity", "crossListCount",
                        "crossListAvailable", "enrollment", "creditHourHigh", "creditHourIndicator", "crossList", "creditHours", "waitCapacity",
                        "waitCount", "id", "openSection", "scheduleTypeDescription", "subjectCourse", "waitAvailable"], 
                        axis=1, inplace=True)
        
        class_df["meetingTimes"] = meeting_infos_list
        
        return class_df
    

    async def get_faculty_by_crn(self, semester_code, crn):
        url = f"https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/getFacultyMeetingTimes?term={semester_code}&courseReferenceNumber={crn}"
        faculty_info = (await self.httpx_client.get(url)).json()["fmt"][0]["faculty"]

        faculty = []
        for prof in faculty_info:
            faculty.append(prof["displayName"])

        return faculty

    # TODO: Add location filters back
    async def add_course_to_list(self, semester_code, subject_code, course_code):
        if (await self.course_already_exists(subject_code, course_code)):
            return

        cur_class_df = await self.add_course(semester_code, subject_code, course_code)

        cur_class_sections = []
        for section in cur_class_df.iterrows():
            sec_dict = section[1].to_dict()
            cur_class_sections.append(sec_dict)

        await self.set_course_color(cur_class_sections[0]["subject"], cur_class_sections[0]["courseNumber"])
        self.all_courses.append(cur_class_sections)

    async def remove_course_from_list(self, subject_code, course_code):
        print(self.all_courses)
        for course in self.all_courses:
            if course[0]["subject"] == subject_code and course[0]["courseNumber"] == course_code:
                self.all_courses.remove(course)
                return True
            
        return False


    async def generate_schedules(self):
        courses_combined_sections = await self.combine_sections()

        each_class_idx = [0] * len(courses_combined_sections)

        total_sch_combos = 1
        for i in range(len(courses_combined_sections)):
            total_sch_combos *= len(courses_combined_sections[i])
        
        all_sch_list = []
        for total_range in range(total_sch_combos):
            cur_schedule_list = []
            for class_num in range(len(courses_combined_sections)):
                cur_schedule_list.append(courses_combined_sections[class_num][each_class_idx[class_num]])

            # Conditions
            if (not overlap_functions.do_any_classes_overlap(cur_schedule_list)):
                """ and not does_overlap_break(cur_schedule_list))"""
                all_sch_list.append(cur_schedule_list)

            # Maintains proper looping
            for back_idx in range(len(each_class_idx) -1, -1, -1):
                if each_class_idx[back_idx] < len(courses_combined_sections[back_idx]) - 1:
                    each_class_idx[back_idx] += 1
                    break
                else:
                    each_class_idx[back_idx] = 0
        
        self.possible_schedules = all_sch_list

    async def combine_sections(self):
        courses_combined_sections = []

        for course in self.all_courses:
            course_sections = []
            used = [False] * len(course)
            
            for i in range(len(course)):
                if used[i]:
                    continue
                    
                cur_section = copy.deepcopy(course[i])
                
                for j in range(i + 1, len(course)):
                    if used[j]:
                        continue
                        
                    if (cur_section["meetingTimes"][0]["beginTime"] == course[j]["meetingTimes"][0]["beginTime"] 
                        and cur_section["meetingTimes"][0]["endTime"] == course[j]["meetingTimes"][0]["endTime"]
                        and cur_section["meetingTimes"][0]["monday"] == course[j]["meetingTimes"][0]["monday"]
                        and cur_section["meetingTimes"][0]["tuesday"] == course[j]["meetingTimes"][0]["tuesday"]
                        and cur_section["meetingTimes"][0]["wednesday"] == course[j]["meetingTimes"][0]["wednesday"]
                        and cur_section["meetingTimes"][0]["thursday"] == course[j]["meetingTimes"][0]["thursday"]
                        and cur_section["meetingTimes"][0]["friday"] == course[j]["meetingTimes"][0]["friday"]):
                        
                        cur_section["sequenceNumber"] += "/" + course[j]["sequenceNumber"]
                        used[j] = True
                
                course_sections.append(cur_section)
            courses_combined_sections.append(course_sections)

        return courses_combined_sections


    async def course_already_exists(self, subject, course_code):
        for existing_course in self.all_courses:
            if subject == existing_course[0]["subject"] and course_code == existing_course[0]["courseNumber"]:
                return True
            
        return False
    
    async def set_course_color(self, subject, course_code):
        colors_list = []
        for color_item in self.course_colors:
            colors_list.append(color_item[2])

        for i in range(8):
            if i not in colors_list:
                self.course_colors.append([subject, course_code, i])
                return i
            
        # Default to first color
        self.course_colors.append([subject, course_code, 0])
        return 0
    
