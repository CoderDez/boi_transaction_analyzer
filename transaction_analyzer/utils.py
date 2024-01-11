import calendar

def get_month_name(month_number):
    try:
        return calendar.month_name[month_number]
    except (IndexError, KeyError):
        return "Invalid month number"