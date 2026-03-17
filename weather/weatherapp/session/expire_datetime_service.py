from datetime import datetime

from django.conf import settings

class ExpireDatetimeService:
    def __init__(self):
        self._expire_datetime_utc: datetime

    def get_new_expire_at(self) -> datetime:
        self._calculate_expare_at()
        return self._expire_datetime_utc

    def _calculate_expare_at(self) -> None:
        delta_unix: float = settings.CUSTOM_SESSION_COOKIE_AGE  # 1 year 0 month 3 days 4 hours 5min 6sec
        current_time_unix: float = datetime.now().timestamp()
        expire_datetime_unix = current_time_unix + delta_unix
        self._expire_datetime_utc = datetime.fromtimestamp(
            expire_datetime_unix, settings.CURRENT_TIMEZONE)

    @staticmethod
    def is_expare_at_valid(expire_at: datetime) -> bool:
        return (expire_at > datetime.now(settings.CURRENT_TIMEZONE))