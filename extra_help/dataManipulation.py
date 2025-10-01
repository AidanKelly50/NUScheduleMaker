import requests
import model as md

def get_terms_dict(max):
    url = f"https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?offset=1&max={max}"

    sems_json = requests.get(url).json()

    return sems_json

spring_sem_code = "202610"

def get_subject_codes(semester_code):
    url = f"https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/get_subject?&term={semester_code}&offset=1&max=300"

    subjects_json = requests.get(url).json()
    return subjects_json

# subject_codes_list and class_codes_list must have same length
def get_class_sections(semester_code, subject_codes_list, class_codes_list):
    if len(subject_codes_list) != len(class_codes_list):
        print("ERROR: getClassSections() line 2")

    # [ class0,     class1,     class2]
    # [[sections], [sections], [sections]]
    list_of_classes_sections = []
    for class_idx in range(len(subject_codes_list)):
        cur_class_sections = []
        cur_class_df = md.get_class_in_semester(semester_code, subject_codes_list[class_idx], class_codes_list[class_idx])
        print("cur_class_df")
        print(cur_class_df)
        for section in cur_class_df.iterrows():
            cur_class_sections.append(section[1].to_dict())
        
        list_of_classes_sections.append(cur_class_sections)
        print(list_of_classes_sections)

    return list_of_classes_sections

def int_to_bool(int):
    if int == 0 or int == 1:
        return int == 1
    
def timedata_to_timestr(hr, min, xm):
    timeint = int(hr) * 100

    if xm == "PM":
        timeint += 1200

    timeint += int(min)

    timestr = str(timeint)
    if len(timestr) == 3:
        timestr = "0" + timestr

    return timestr