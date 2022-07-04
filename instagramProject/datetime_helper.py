from datetime import datetime, timedelta, time
from django.utils import timezone


class DatetimeHelper:
    @staticmethod
    def get_range_date_today():
        today_min = datetime.combine(timezone.now(), time.min)
        today_max = datetime.combine(timezone.now(), time.max)
        return today_min, today_max

    @staticmethod
    def get_time_threshold():
        return timezone.now() - timedelta(hours=24)
