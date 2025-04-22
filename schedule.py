import datetime

class Schedule:
    def __init__(self):
        self.schedule = {
            "星期一": ["数学", "英语", "物理"],
            "星期二": ["生物", "化学", "历史"],
            "星期三": ["地理", "艺术", "体育"],
            "星期四": ["计算机科学", "音乐", "经济学"],
            "星期五": ["文学", "哲学", "社会学"]
        }

    def get_today_schedule(self):
        weekday_map = {
            0: "星期一",
            1: "星期二",
            2: "星期三",
            3: "星期四",
            4: "星期五",
            5: "星期六",
            6: "星期日"
        }
        today_weekday = datetime.datetime.today().weekday()
        return self.schedule.get(weekday_map[today_weekday], [])