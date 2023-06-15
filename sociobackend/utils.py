# from django.utils.timezone import now
# from django.utils.timesince import timesince
# from dateutil.relativedelta import relativedelta
# from datetime import datetime


# def time_formating(input_time):
#     """   Converts the given `created_at` date into a human-readable string.
#     """
#     time_since = timesince(input_time, now())
#     # Return the time difference in a human-readable format
#     if int(time_since[0:1]) <= 0:
#         return f"just now"
#     elif "minute" in time_since:
#         return f"{time_since.split(',')[0]} ago"
#     elif "hour" in time_since:
#         return f"{time_since.split(',')[0]} ago"
#     elif "day" in time_since:
#         return f"{time_since.split(',')[0]} ago"
#     elif "week" in time_since:
#         return f"{time_since.split(',')[0]} ago"
#     elif "month" in time_since:
#         months = relativedelta(datetime.now(), input_time).months
#         if months == 1:
#             return f"{months} month ago"
#         else:
#             return f"{months} months ago"
#     else:
#         return input_time.strftime("%Y-%m-%d %H:%M:%S")



from datetime import datetime
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta


def time_formating(input_time):
    """Converts the given `created_at` date into a human-readable string."""
    now_time = now()
    time_diff = relativedelta(now_time, input_time)

    if time_diff.years > 0:
        if time_diff.years == 1:
            return f"{time_diff.years} year ago"
        else:
            return f"{time_diff.years} years ago"
    elif time_diff.months > 0:
        if time_diff.months == 1:
            return f"{time_diff.months} month ago"
        else:
            return f"{time_diff.months} months ago"
    elif time_diff.days > 0:
        if time_diff.days == 1:
            return f"{time_diff.days} day ago"
        else:
            return f"{time_diff.days} days ago"
    elif time_diff.hours > 0:
        if time_diff.hours == 1:
            return f"{time_diff.hours} hour ago"
        else:
            return f"{time_diff.hours} hours ago"
    elif time_diff.minutes > 0:
        if time_diff.minutes == 1:
            return f"{time_diff.minutes} minute ago"
        else:
            return f"{time_diff.minutes} minutes ago"
    else:
        return "just now"
