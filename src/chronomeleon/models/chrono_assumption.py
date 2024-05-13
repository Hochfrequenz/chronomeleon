"""contains the ChronoAssumption class"""

from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from pytz import BaseTzInfo


@dataclass(frozen=True, kw_only=True)
class ChronoAssumption:
    """
    represents assumptions about how a specific system interprets a specific field that holds date or time
    """

    resolution: Optional[timedelta] = None
    """
    This is only necessary to provide, if the field is an inclusive end date.
    The smallest unit of time that this field can represent.
    Typically this is something like 1 day, 1 second, 1 microsecond.
    Adding one "unit" of the resolution leads to the smallest possible increase in the field.
    If e.g. the resolution is 1 day, then the next possible value after 2024-01-01 is 2024-01-02.
    But if the resolution is 1 second, then the next possible value after 2024-01-01 00:00:00 is 2024-01-01 00:00:01.
    """

    implicit_timezone: Optional[BaseTzInfo] = None
    """
    Systems often don't provide an explicit UTC offset with their date or time fields.
    In this case, the system implicitly uses a specific timezone.
    You can specific this implicit timezone here.
    If the datetimes come with a specified UTC offset, leave it None.
    You have to specify the implicit timezone as a pytz-timezone object, e.g. pytz.timezone("Europe/Berlin").
    pytz is a dependency of chronomeleon; If you install chronomeleon, you also get pytz.
    """

    is_inclusive_end: Optional[bool] = None
    """
    Must not be None if is_end is True.
    True if and only if the end of the range is inclusive.
    If the resolution is timedelta(days=1) and is_inclusive_end is True, then the range 2024-01-01 to 2024-01-31 covers
    the entire month of January.
    If is_inclusive_end is False, then the range 2024-01-01 to 2024-02-01 covers the entire month of January.
    """

    is_gastag_aware: bool = False
    """
    True if and only if the start of a day is 6:00 am German local time.
    If you never heard of the "Gastag", you can ignore this parameter and let it default to False.
    """

    is_date_only: bool = False
    """
    True if and only if the field in the respective system is a date without a time component (datetime.date).
    """

    def get_consistency_errors(self) -> list[str]:
        """
        returns errors from the self-consistency check; if the returned list is empty, the object is self-consistent
        """
        result: list[str] = []
        if self.is_inclusive_end and self.resolution is None:
            result.append("if is_inclusive_end is True, then resolution must be set")
        if self.resolution is not None and not isinstance(self.resolution, timedelta):
            result.append(f"resolution must be a timedelta object but is {self.resolution.__class__.__name__}")
        if self.implicit_timezone is not None and not isinstance(self.implicit_timezone, BaseTzInfo):
            result.append(
                f"implicit_timezone must be a pytz timezone object but is {self.implicit_timezone.__class__.__name__}"
            )
        return result

    def is_self_consistent(self) -> bool:
        """
        returns True if the object is self-consistent
        """
        return not any(self.get_consistency_errors())
