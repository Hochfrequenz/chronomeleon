"""
models are the classes used by chronomeleon
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from pytz import timezone


@dataclass(frozen=True, kw_only=True)
class ChronoAssumption:
    """
    represents assumptions about how a specific system interprets a specific field that holds date or time
    """

    resolution: timedelta
    """
    The smallest unit of time that this field can represent.
    Typically this is something like 1 day, 1 second, 1 microsecond.
    Adding one "unit" of the resolution leads to the smallest possible increase in the field.
    If e.g. the resolution is 1 day, then the next possible value after 2024-01-01 is 2024-01-02.
    But if the resolution is 1 second, then the next possible value after 2024-01-01 00:00:00 is 2024-01-01 00:00:01.
    """

    implicit_timezone: Optional[timezone] = None
    """
    Systems often don't provide an explicit UTC offset with their date or time fields.
    In this case, the system implicitly uses a specific timezone.
    You can specific this implicit timezone here.
    If the datetimes come with a specified UTC offset, leave it None.
    You have to specify the implicit timezone as a pytz-timezone object, e.g. pytz.timezone("Europe/Berlin").
    pytz is a dependency of chronomeleon; If you install chronomeleon, you also get pytz.
    """

    is_end: Optional[bool] = None
    """
    True if and only if the date or time is the end of a range. None if it doesn't matter.
    """

    is_inclusive_end: Optional[bool] = None
    """
    Must not be None if is_end is True.
    True if and only if the end of the range is inclusive.
    If the resolution is timedelta(days=1) and is_inclusive_end is True, then the range 2024-01-01 to 2024-01-31 covers
    the entire month of January.
    If is_inclusive_end is False, then the range 2024-01-01 to 2024-02-01 covers the entire month of January.
    """
