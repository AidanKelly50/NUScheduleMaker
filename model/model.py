from typing import Dict
import requests
import pandas as pd

from model.Break import *
import model.schedule_time as st

from model.Schedule import Schedule

import extra_help.dataManipulation as dm

class Model:
    def __init__(self):
        self.cur_semester = ""
        self.all_classes_all_sections = []

        self.breaks_list = [Break("0830", "1100", [True, False, True, False, False])]

    def set_cur_semester(self, sem_string):
        if sem_string == "Choose Semester":
            return

        sems_list = self.get_semesters()
        for sem in sems_list:
            if sem["description"] == sem_string:
                self.cur_semester = sem["code"]

    def get_class_sections(self):
        return self.all_classes_all_sections
    
    def get_breaks(self):
        return self.breaks_list

    def get_class_in_semester(self, semester_code, subject_code, class_code):
        # SET TERM
        # Define the URL and term code
        url = "https://nubanner.neu.edu/StudentRegistrationSsb/ssb/term/search"

        # Headers and data for the request
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",}
        data = {"term": semester_code,
                "studyPath": "",
                "studyPathText": "",
                "startDatepicker": "",
                "endDatepicker": ""}

        # Make the POST request
        post_response = requests.post(url, headers=headers, data=data)
        # Check the response
        if post_response.status_code != 200:
            print(f"Failed to declare term. Status code: {post_response.status_code}")
            print(post_response.text)
        # Get cookie data
        cookie_jar = post_response.cookies
        cookies_dict = {cookie.name: cookie.value for cookie in cookie_jar}

        # GET CLASS DATA
        # Define the base URL for course search
        base_url = "https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults"

        # Define the search parameters and headers
        params = {"txt_subject": subject_code,
                "txt_courseNumber": class_code,
                "txt_term": semester_code,  # Use the term code previously declared
                "pageOffset": 0,
                "pageMaxSize": 100,
                "sortColumn": "subjectDescription",
                "sortDirection": "asc"}
        headers = {"Content-Type": "application/json"}

        # Make the GET request to retrieve course data
        class_response = requests.get(base_url, headers=headers, params=params, cookies=cookies_dict)
        # Check the response
        if class_response.status_code != 200:
            print(f"Failed to retrieve course data. Status code: {class_response.status_code}")
            print(class_response.json())

        # BRING OUT MEETING INFO
        meeting_infos_list = []
        cr_json_data = class_response.json()["data"]
        print("Hello", cr_json_data)

        for cur_section in cr_json_data:
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
        class_df = pd.DataFrame(class_response.json()["data"])
        class_df.drop(["term", "termDesc", "partOfTerm", "courseNumber", "subject", "subjectDescription", "linkIdentifier", "isSectionLinked", 
                        "instructionalMethodDescription", "meetingsFaculty", "reservedSeatSummary", "sectionAttributes", "crossListCapacity", "crossListCount",
                        "crossListAvailable", "enrollment", "creditHourHigh", "creditHourIndicator", "crossList", "creditHours", "waitCapacity",
                        "waitCount", "id", "openSection", "scheduleTypeDescription"], 
                        axis=1, inplace=True)

        class_df["meetingTimes"] = meeting_infos_list

        return class_df

    def add_class_to_list(self, subject_code, class_code, location):
        cur_class_df = self.get_class_in_semester(self.cur_semester, subject_code, class_code)

        cur_class_sections = []
        for section in cur_class_df.iterrows():
            sec_dict = section[1].to_dict()
            if sec_dict["campusDescription"] == location:
                cur_class_sections.append(sec_dict)
            elif sec_dict["campusDescription"] == "Online":
                cur_class_sections.append(sec_dict)
        
        self.all_classes_all_sections.append(cur_class_sections)


    def get_section_text_summary(self, sec : Dict[str, list[str, int]]):
        answer = "  Section: " + sec["sequenceNumber"] + " | CRN: " + sec["courseReferenceNumber"] + " | "

        if sec["campusDescription"] == "Online":
            answer += "Online "

        times_list = sec["meetingTimes"]
        if times_list[0]["monday"] or times_list[0]["tuesday"] or times_list[0]["wednesday"] or times_list[0]["thursday"] or times_list[0]["friday"]:
            for time in times_list:
                if time["monday"]:
                    answer += "M"
                if time["tuesday"]:
                    answer += "T"
                if time["wednesday"]:
                    answer += "W"
                if time["thursday"]:
                    answer += "R"
                if time["friday"]:
                    answer += "F"
                answer += " " + self.str_to_timestr(time["beginTime"]) + "-" + self.str_to_timestr(time["endTime"]) + ", "
            answer = answer[0:len(answer) - 2] # Remove last ", "
        else:
            answer += "Async"

        answer += "\n      "
        

        answer += "Prof: " 
        if len(sec["faculty"]) > 0:
            answer += sec["faculty"][0]
        else:
            answer += "TBD"
        answer += " | Seats Left: " + str(sec["seatsAvailable"]) + "/" + str(sec["maximumEnrollment"])
        return answer
    
    def get_break_datetime_text(self, brk):
        start_time, end_time, days_list = brk.get_break_time_data()
        answer = ""

        if days_list[0]:
            answer += "M"
        if days_list[1]:
            answer += "T"
        if days_list[2]:
            answer += "W"
        if days_list[3]:
            answer += "R"
        if days_list[4]:
            answer += "F"
        
        answer += " " + self.str_to_timestr(start_time) + "-" + self.str_to_timestr(end_time)
        return answer
        

    def str_to_timestr(self, start_str):
        hr_num = int(start_str[0:2])
        min_num = int(start_str[2:4])

        answer = ""

        if hr_num > 12:
            hr_num -= 12
        
        answer += str(hr_num)
        answer += ":"
        answer += f"{min_num:02d}"
        return answer

        
    def select_section(self, crn):
        for cls in range(len(self.all_classes_all_sections)):
            sec_to_save = []
            for sec in range(len(self.all_classes_all_sections[cls])):
                if self.all_classes_all_sections[cls][sec]["courseReferenceNumber"] == crn:
                    sec_to_save.append(self.all_classes_all_sections[cls][sec])
                    self.all_classes_all_sections[cls] = sec_to_save
                    return

    def remove_section(self, crn):
        for cls in range(len(self.all_classes_all_sections)):
            for sec in range(len(self.all_classes_all_sections[cls])):
                if self.all_classes_all_sections[cls][sec]["courseReferenceNumber"] == crn:
                    self.all_classes_all_sections[cls].remove(self.all_classes_all_sections[cls][sec])
                    return
                
    def remove_class(self, code):
        for cls in range(len(self.all_classes_all_sections)):
            if self.all_classes_all_sections[cls][0]["subjectCourse"] == code:
                self.all_classes_all_sections.remove(self.all_classes_all_sections[cls])
                return
            
    def generate_schedules(self):
        return self.get_schedule_options(self.all_classes_all_sections)

    def get_schedule_options(self, list_of_classes_sections):
        each_class_idx = [0] * len(list_of_classes_sections)

        total_sch_combos = 1
        for i in range(len(list_of_classes_sections)):
            total_sch_combos *= len(list_of_classes_sections[i])
        
        all_sch_list = []
        for total_range in range(total_sch_combos):
            cur_schedule_list = []
            for class_num in range(len(list_of_classes_sections)):
                cur_schedule_list.append(list_of_classes_sections[class_num][each_class_idx[class_num]])
            
            # Conditions
            if (not st.do_any_classes_overlap(cur_schedule_list)):
                """ and not does_overlap_break(cur_schedule_list))"""
                all_sch_list.append(Schedule(cur_schedule_list))

            # Maintains proper looping
            for back_idx in range(len(each_class_idx) -1, -1, -1):
                if each_class_idx[back_idx] < len(list_of_classes_sections[back_idx]) - 1:
                    each_class_idx[back_idx] += 1
                    break
                else:
                    each_class_idx[back_idx] = 0
        
        return all_sch_list

    def add_break(self, begin, end, mon, tues, wed, thurs, fri):
        self.breaks_list.append(Break(begin, end, [mon, tues, wed, thurs, fri]))


    def get_semesters(self):
        sems_url = "https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?offset=1&max=14"
        sems_json = requests.get(sems_url).json()
        return sems_json

    def remove_break(self, brk):
        self.breaks_list.remove(brk)

    def does_overlap_break(self):
        print("hi")
