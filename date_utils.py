import datetime
from lunardate import LunarDate

def lunar_to_solar(lunar_month, lunar_day, year=None):
    """将农历日期转换为阳历日期"""
    year = year or datetime.datetime.now().year
    try:
        lunar = LunarDate(year, lunar_month, lunar_day)
        return lunar.toSolarDate()
    except ValueError:
        return datetime.date(year, lunar_month, lunar_day)

def get_days_until(target_month, target_day, is_lunar=False):
    """计算距离目标日期的天数"""
    today = datetime.datetime.now().date()
    
    if is_lunar:
        target_date = lunar_to_solar(target_month, target_day, today.year)
        if target_date < today:
            target_date = lunar_to_solar(target_month, target_day, today.year + 1)
    else:
        target_date = datetime.date(today.year, target_month, target_day)
        if target_date < today:
            target_date = datetime.date(today.year + 1, target_month, target_day)
    
    return (target_date - today).days