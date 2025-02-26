import tkinter as tk
import model.schedule_time as ts

class Schedule:
    def __init__(self, given_classes):
        self.classes: list = given_classes

    
    def draw_schedule(self, frame, cur_row, colors_list):
        late_sch_added = 0
        for cls in self.classes:
            c1Begin = cls["meetingTimes"][0]["beginTime"]
            c1End = cls["meetingTimes"][0]["endTime"]
            c1Days = [cls["meetingTimes"][0]["monday"], cls["meetingTimes"][0]["tuesday"], cls["meetingTimes"][0]["wednesday"], 
                        cls["meetingTimes"][0]["thursday"], cls["meetingTimes"][0]["friday"]]
            c2Begin = "1800"
            c2End = "2200"
            c2Days = [True] * 5

            if ts.do_two_timeblocks_overlap(c1Begin, c1End, c1Days, c2Begin, c2End, c2Days):
                late_sch_added = 4

        canvas = tk.Canvas(frame, width=353, height=160 + (late_sch_added * 16), bg="white")
        canvas.grid(row=cur_row, column=0, padx=5, pady=5, sticky="w")

        # Draw hour lines
        for i in range(12 + late_sch_added):
            canvas.create_line(30, 16 * i + 3, 455, 16 * i + 3, fill="lightgray", width=0.5)

            cvs_txt = f"{i + 8}am"
            if i > 4:
                cvs_txt = f"{i - 4}pm"
            elif i == 4:
                cvs_txt = f"{i + 8}pm"
            canvas.create_text(15, 16 * i + 3, text=cvs_txt, font=("Calibri", 7))

        # Draw Day Lines
        for i in range(6):
            canvas.create_line(i * 65 + 30, 0, i * 65 + 30, 285, fill="lightgray", width=1)

        contains_online_async = False
        # Draw classes
        color_count = 0
        for cls in self.classes:
            color = colors_list[color_count]
            color_count += 1
            
            
            if cls["campusDescription"] != "Online" or cls["meetingTimes"][0]["beginTime"] != None:
                time_slots = cls["meetingTimes"]
                for time in time_slots:
                    cvs_y = self.get_canvas_y(time["beginTime"])
                    cvs_end_y = self.get_canvas_y(time["endTime"])

                    y_offset = 4
                    if time["monday"]:
                        canvas.create_rectangle(31, cvs_y + y_offset, 95, cvs_end_y + y_offset, fill=color, outline="")
                        canvas.create_text(63, cvs_y + y_offset - 1 + ((cvs_end_y - cvs_y) / 2), text=cls["subjectCourse"] + " - " + cls["sequenceNumber"], font=("Calibri", 7))
                    if time["tuesday"]:
                        canvas.create_rectangle(96, cvs_y + y_offset, 160, cvs_end_y + y_offset, fill=color, outline="")
                        canvas.create_text(128, cvs_y + y_offset - 1 + ((cvs_end_y - cvs_y) / 2), text=cls["subjectCourse"] + " - " + cls["sequenceNumber"], font=("Calibri", 7))
                    if time["wednesday"]:
                        canvas.create_rectangle(161, cvs_y + y_offset, 225, cvs_end_y + y_offset, fill=color, outline="")
                        canvas.create_text(193, cvs_y + y_offset - 1 + ((cvs_end_y - cvs_y) / 2), text=cls["subjectCourse"] + " - " + cls["sequenceNumber"], font=("Calibri", 7))
                    if time["thursday"]:
                        canvas.create_rectangle(226, cvs_y + y_offset, 290, cvs_end_y + y_offset, fill=color, outline="")
                        canvas.create_text(258, cvs_y + y_offset - 1 + ((cvs_end_y - cvs_y) / 2), text=cls["subjectCourse"] + " - " + cls["sequenceNumber"], font=("Calibri", 7))
                    if time["friday"]:
                        canvas.create_rectangle(291, cvs_y + y_offset, 355, cvs_end_y + y_offset, fill=color, outline="")
                        canvas.create_text(323, cvs_y + y_offset - 1 + ((cvs_end_y - cvs_y) / 2), text=cls["subjectCourse"] + " - " + cls["sequenceNumber"], font=("Calibri", 7))
            else:
                canvas.create_text(290, 155, text="Online Async: " + cls["subjectCourse"] + " - " + cls["sequenceNumber"], font=("Calibri", 7))
                contains_online_async = True

        return contains_online_async

        
    
    def get_canvas_y(self, time_str):
        hr_num = int(time_str[0:2])
        min_num = int(time_str[2:4])

        y_pos = (hr_num - 8) * 16
        y_pos += (min_num / 60) * 16
        return y_pos
