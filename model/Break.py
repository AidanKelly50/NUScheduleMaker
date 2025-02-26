

class Break:
    def __init__(self, begin_time, end_time, day_bools):
        self.begin_time = begin_time
        self.end_time = end_time
        self.day_bools: list = day_bools

    def get_break_time_data(self):
        return self.begin_time, self.end_time, self.day_bools
        
        