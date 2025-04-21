import datetime

class Schedule:
    def __init__(self):
        self.schedule = {
            "Monday": ["Math", "English", "Physics"],
            "Tuesday": ["Biology", "Chemistry", "History"],
            "Wednesday": ["Geography", "Art", "Physical Education"],
            "Thursday": ["Computer Science", "Music", "Economics"],
            "Friday": ["Literature", "Philosophy", "Sociology"]
        }

    def get_today_schedule(self):
        today = datetime.datetime.today().strftime('%A')
        return self.schedule.get(today, [])