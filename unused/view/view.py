import tkinter as tk
from tkinter import ttk
from tkinter import *
import model.model as mdl
from model.Schedule import *
import extra_help.dataManipulation as dm


class Window(tk.Tk):

    def __init__(self):
        super().__init__()

        self.model = mdl.Model()

        self.subj_code = tk.StringVar()
        self.cls_code = tk.StringVar()

        self.colors_list = ["#FFB1B0", "#A9D1F7", "#FFDFBE", "#B4F0A7", "#FFFFBF", "#CC99FF", "#FFBDC7", "#A0A0C9",
                            "CFF8F8"]

        self.title("NU Schedule Maker")
        self.geometry("1200x750")

        # Set up a container frame to hold the left and right scrollable areas
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Left scrollable area setup
        left_frame = ttk.Frame(container)
        left_frame.grid(row=0, column=0, sticky="nsew")

        self.left_canvas = tk.Canvas(left_frame)
        self.left_canvas.grid(row=0, column=0, sticky="nsew")

        self.left_scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.left_canvas.yview)
        self.left_scrollbar.grid(row=0, column=1, sticky="ns")

        self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)

        # Frame inside left canvas
        self.left_scrollable_frame = ttk.Frame(self.left_canvas)
        self.left_canvas.create_window((0, 0), window=self.left_scrollable_frame, anchor="nw")

        # Bind the function to update the scroll region whenever the frame size changes
        self.left_scrollable_frame.bind("<Configure>", self.update_scroll_region_left)

        # Populate left scrollable frame
        self.populate_left_frame()

        # Bind mouse scroll to left canvas
        self.bind_scroll(self.left_canvas)

        # Right scrollable area setup
        right_frame = ttk.Frame(container)
        right_frame.grid(row=0, column=1, sticky="nsew")

        self.right_canvas = tk.Canvas(right_frame)
        self.right_canvas.grid(row=0, column=0, sticky="nsew")

        self.right_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.right_canvas.yview)
        self.right_scrollbar.grid(row=0, column=1, sticky="ns")

        self.right_canvas.configure(yscrollcommand=self.right_scrollbar.set)

        # Frame inside right canvas
        self.right_scrollable_frame = ttk.Frame(self.right_canvas)
        self.right_canvas.create_window((0, 0), window=self.right_scrollable_frame, anchor="nw")

        # Bind the function to update the scroll region whenever the frame size changes
        self.right_scrollable_frame.bind("<Configure>", self.update_scroll_region_right)

        # Populate right scrollable frame
        self.populate_right_frame()

        # Bind mouse scroll to right canvas
        self.bind_scroll(self.right_canvas)

        # Expand the frames to make full use of space
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

    def bind_scroll(self, canvas):
        """Bind mouse scroll events to a canvas when the pointer is over it."""
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e, canvas)))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    def _on_mousewheel(self, event, canvas):
        """Handle mouse wheel scrolling for the specific canvas under the mouse pointer."""
        if event.delta > 0:
            canvas.yview_scroll(-1, "units")
        else:
            canvas.yview_scroll(1, "units")

    def update_scroll_region_left(self, event=None):
        """Update scroll region for left canvas based on the frame's bounding box."""
        self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))

    def update_scroll_region_right(self, event=None):
        """Update scroll region for right canvas based on the frame's bounding box."""
        self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all"))

    def populate_left_frame(self):
        """Populate a given frame with a specified number of labeled elements."""
        frame = self.left_scrollable_frame
        self.clear_frame(frame)
        cur_row = 0

        ttk.Label(frame, text="Semester", font=("Calibri", 24, "bold")).grid(row=cur_row, column=0, padx=5, pady=5,
                                                                             columnspan=5, sticky="w")

        clicked_sem = StringVar()
        clicked_sem.set("Choose Semester")

        sems_list = self.model.get_semesters()
        sems_text_list = ["Choose Semester"] + [d["description"] for d in sems_list]

        ttk.OptionMenu(frame, clicked_sem, *sems_text_list,
                       command=lambda cls=clicked_sem
                       : self.model.set_cur_semester(cls)).grid(row=0, column=1, padx=5, pady=5, columnspan=4, sticky="w")
        cur_row += 1

        ttk.Label(frame, text="Breaks", font=("Calibri", 24, "bold")).grid(row=cur_row, column=0, padx=5, pady=5,
                                                                           columnspan=5, sticky="w")
        cur_row += 1

        hours_list = ["H", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        mins_list = ["M", "00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
        ampm_list = ["XM", "AM", "PM"]

        ttk.Label(frame, text="Start:", font=("Calibri", 14)).grid(row=cur_row, column=0, padx=(10, 0), pady=5, sticky="w")

        clicked_start_hour = StringVar()
        clicked_start_min = StringVar()
        clicked_start_ampm = StringVar()

        ttk.OptionMenu(frame, clicked_start_hour, *hours_list).grid(row=cur_row, column=1, padx=5, pady=5, sticky="e")
        ttk.OptionMenu(frame, clicked_start_min, *mins_list).grid(row=cur_row, column=2, padx=5, pady=5, sticky="w")
        ttk.OptionMenu(frame, clicked_start_ampm, *ampm_list).grid(row=cur_row, column=3, padx=5, pady=5, sticky="w")

        cur_row += 1
        ttk.Label(frame, text="End:", font=("Calibri", 14)).grid(row=cur_row, column=0, padx=(10, 0), pady=5,
                                                                 sticky="w")

        clicked_end_hour = StringVar()
        clicked_end_min = StringVar()
        clicked_end_ampm = StringVar()

        ttk.OptionMenu(frame, clicked_end_hour, *hours_list).grid(row=cur_row, column=1, padx=5, pady=5, sticky="e")
        ttk.OptionMenu(frame, clicked_end_min, *mins_list).grid(row=cur_row, column=2, padx=5, pady=5, sticky="w")
        ttk.OptionMenu(frame, clicked_end_ampm, *ampm_list).grid(row=cur_row, column=3, padx=5, pady=5, sticky="w")

        cur_row += 1
        check_m = IntVar()
        ttk.Checkbutton(frame, variable=check_m, text="Monday").grid(row=cur_row, column=0, padx=5, pady=5, sticky="w")
        check_t = IntVar()
        ttk.Checkbutton(frame, variable=check_t, text="Tuesday").grid(row=cur_row, column=1, padx=5, pady=5, sticky="w")
        check_w = IntVar()
        ttk.Checkbutton(frame, variable=check_w, text="Wednesday").grid(row=cur_row, column=2, padx=5, pady=5, sticky="w")
        check_r = IntVar()
        ttk.Checkbutton(frame, variable=check_r, text="Thursday").grid(row=cur_row, column=3, padx=5, pady=5, sticky="w")
        check_f = IntVar()
        ttk.Checkbutton(frame, variable=check_f, text="Friday").grid(row=cur_row, column=4, padx=5, pady=5, sticky="w")

        cur_row += 1
        ttk.Button(frame, text="+ Add Break",
                   command=lambda sh=clicked_start_hour, sm=clicked_start_min, sxm=clicked_start_ampm,
                                  eh=clicked_end_hour, em=clicked_end_min, exm=clicked_end_ampm,
                                  m=check_m, t=check_t, w=check_w, r=check_r, f=check_f:
                   self.add_break(sh, sm, sxm, eh, em, exm, m, t, w, r, f)).grid(
            row=cur_row, column=0, padx=5, pady=5, sticky="w")

        cur_row += 1
        breaks_list = self.model.get_breaks()
        for brk in breaks_list:
            brk_text = self.model.get_break_datetime_text(brk)
            ttk.Label(frame, text="Break:", font=("Calibri", 14)).grid(row=cur_row, column=0, padx=(0, 0), pady=5, sticky="e")
            ttk.Label(frame, text=brk_text, font=("Calibri", 14)).grid(row=cur_row, column=1, padx=(10, 0), pady=5, sticky="w")
            ttk.Button(frame, text="Remove", command=lambda cur_brk=brk
            : self.remove_break(cur_brk)).grid(row=cur_row, column=2, padx=5, pady=5, sticky="w")
            cur_row += 1

        ttk.Label(frame, text="Courses", font=("Calibri", 24, "bold")).grid(row=cur_row, column=0, padx=5, pady=5,
                                                                            columnspan=5, sticky="w")
        cur_row += 1
        ttk.Button(frame, text="+ Add Class", command=self.add_class_button).grid(row=cur_row, column=0, padx=5, pady=5,
                                                                                  sticky="w")
        ttk.Label(frame, text="Subject Code:", font=("Calibri", 14)).grid(row=cur_row, column=1, padx=(10, 0), pady=5, sticky="e")
        ttk.Entry(frame, textvariable=self.subj_code, width=8).grid(row=cur_row, column=2, pady=5, sticky="w")
        ttk.Label(frame, text="Class Code:", font=("Calibri", 14)).grid(row=cur_row, column=3, padx=(10, 0), pady=5,
                                                                        sticky="e")
        ttk.Entry(frame, textvariable=self.cls_code, width=8).grid(row=cur_row, column=4, pady=5, sticky="w")
        cur_row += 1

        all_classes_sections = self.model.get_class_sections()
        for cls_info in all_classes_sections:
            ttk.Label(frame, text=" ", font=("Calibri", 6)).grid(row=cur_row, column=0, columnspan=5)
            cur_row += 1

            class_text = cls_info[0]["subjectCourse"] + ": " + cls_info[0]["courseTitle"]
            ttk.Label(frame, text=class_text, font=("Calibri", 18)).grid(row=cur_row, column=0, padx=5, pady=(8, 0),
                                                                         columnspan=5, sticky="w")
            ttk.Button(frame, text="Remove",
                       command=lambda cls=cls_info[0]["subjectCourse"]: self.remove_class_view(cls)).grid(row=cur_row,
                                                                                                          column=4,
                                                                                                          sticky="e",
                                                                                                          padx=(5, 0))
            cur_row += 1

            for sec_info in cls_info:
                sec_text = self.model.get_section_text_summary(sec_info)
                ttk.Label(frame, text=sec_text, font=("Calibri", 12)).grid(row=cur_row, column=0, columnspan=3,
                                                                           sticky="w", padx=5, pady=(0, 3))
                ttk.Button(frame, text="Select",
                           command=lambda crn=sec_info["courseReferenceNumber"]: self.select_section_view(crn)).grid(
                    row=cur_row, column=3, sticky="e", padx=(50, 5))
                ttk.Button(frame, text="Remove",
                           command=lambda crn=sec_info["courseReferenceNumber"]: self.remove_section_view(crn)).grid(
                    row=cur_row, column=4, sticky="e", padx=(5, 0))
                cur_row += 1

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def add_class_button(self):
        subject_code = self.subj_code.get()
        class_code = self.cls_code.get()
        self.model.add_class_to_list(subject_code, class_code, "Boston")
        self.subj_code.set("")
        self.cls_code.set("")
        self.populate_left_frame()

    def remove_class_view(self, code):
        self.model.remove_class(code)
        self.populate_left_frame()

    def select_section_view(self, crn):
        self.model.select_section(crn)
        self.populate_left_frame()

    def remove_section_view(self, crn):
        self.model.remove_section(crn)
        self.populate_left_frame()

    def populate_right_frame(self):
        frame = self.right_scrollable_frame
        self.clear_frame(frame)
        ttk.Label(frame, text="Possible Schedules", font=("Calibri", 24, "bold")).grid(row=0, column=0, padx=5, pady=5,
                                                                                       columnspan=2, sticky="w")
        ttk.Button(frame, text="Generate", command=self.generate_schedules).grid(row=0, column=2, padx=5, pady=5,
                                                                                 sticky="e")

    def generate_schedules(self):
        frame = self.right_scrollable_frame
        self.populate_right_frame()
        all_possible_schedules = self.model.generate_schedules()
        for i in range(len(all_possible_schedules)):
            schedule: Schedule = all_possible_schedules[i]
            schedule.draw_schedule(frame, i + 1, self.colors_list)

    def add_break(self, start_hour, start_min, start_xm, end_hour, end_min, end_xm, m, t, w, r, f):
        print(m.get(), t.get(), w.get(), r.get(), f.get())
        self.model.add_break(dm.timedata_to_timestr(start_hour.get(), start_min.get(), start_xm),
                             dm.timedata_to_timestr(end_hour.get(), end_min.get(), end_xm),
                             dm.int_to_bool(m.get()), dm.int_to_bool(t.get()), dm.int_to_bool(w.get()),
                             dm.int_to_bool(r.get()), dm.int_to_bool(f.get()))
        self.populate_left_frame()

    def remove_break(self, brk):
        self.model.remove_break(brk)
        self.populate_left_frame()
