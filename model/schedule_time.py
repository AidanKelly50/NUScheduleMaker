def do_any_classes_overlap(classes_list):
    for c1 in range(len(classes_list)):
        for c2 in range(c1 + 1, len(classes_list)):
            c1Begin = str
            c1End = str
            c2Begin = str
            c2End = str

            c1Begin, c1End, c1Days = get_class_time_data(classes_list[c1], 0)
            c2Begin, c2End, c2Days = get_class_time_data(classes_list[c2], 0)
            if do_two_timeblocks_overlap(c1Begin, c1End, c1Days, c2Begin, c2End, c2Days):
                return True
            
            if len(classes_list[c1]["meetingTimes"]) == 2:
                c1Begin, c1End, c1Days = get_class_time_data(classes_list[c1], 1)
                c2Begin, c2End, c2Days = get_class_time_data(classes_list[c2], 0)
                if do_two_timeblocks_overlap(c1Begin, c1End, c1Days, c2Begin, c2End, c2Days):
                    return True
                
            if len(classes_list[c2]["meetingTimes"]) == 2:
                c1Begin, c1End, c1Days = get_class_time_data(classes_list[c1], 0)
                c2Begin, c2End, c2Days = get_class_time_data(classes_list[c2], 1)
                if do_two_timeblocks_overlap(c1Begin, c1End, c1Days, c2Begin, c2End, c2Days):
                    return True

            if len(classes_list[c1]["meetingTimes"]) == 2 and len(classes_list[c2]["meetingTimes"]) == 2:
                c1Begin, c1End, c1Days = get_class_time_data(classes_list[c1], 1)
                c2Begin, c2End, c2Days = get_class_time_data(classes_list[c2], 1)
                if do_two_timeblocks_overlap(c1Begin, c1End, c1Days, c2Begin, c2End, c2Days):
                    return True
    
    return False

def get_class_time_data(cls, time_idx):
    cBegin = cls["meetingTimes"][time_idx]["beginTime"]
    cEnd = cls["meetingTimes"][time_idx]["endTime"]
    cDays = [cls["meetingTimes"][time_idx]["monday"], cls["meetingTimes"][time_idx]["tuesday"], cls["meetingTimes"][time_idx]["wednesday"], 
                cls["meetingTimes"][time_idx]["thursday"], cls["meetingTimes"][time_idx]["friday"]]
    
    return cBegin, cEnd, cDays


# def does_overlap_break(classes_list, breaks_list):
#     for brk in breaks_list:
#         for cls in classes_list:
#             c1Begin, c1End, c1Days = get_class_time_data(classes_list[cls], 0)
#             c2Begin, c2End, c2Days = brk.get_break_time_data()
#             if do_two_timeblocks_overlap(c1Begin, c1End, c1Days, c2Begin, c2End, c2Days):
#                 return True
            
#             if len(cls["meetingTimes"]) == 2:
#                 c1Begin, c1End, c1Days = get_class_time_data(cls, 1)
#                 c2Begin, c2End, c2Days = brk.get_break_time_data()
#                 if do_two_timeblocks_overlap(c1Begin, c1End, c1Days, c2Begin, c2End, c2Days):
#                     return True
    
#     return False

def do_two_timeblocks_overlap(c1Begin, c1End, c1Days, c2Begin, c2End, c2Days):
    for i in range(len(c1Days)):
            if c1Days[i] == True and c2Days[i] == True:
                if int(c2Begin) >= int(c1Begin) and int(c2Begin) < int(c1End):
                    return True
                elif int(c2End) > int(c1Begin) and int(c2End) <= int(c1End): 
                    return True
                elif int(c1Begin) >= int(c2Begin) and int(c1End) <= int(c2End):
                    return True

    return False