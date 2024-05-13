"""
This a docstring for the module.
"""
import datetime as dt_module
from datetime import date, datetime, timedelta, timezone
from typing import Union

import pytz

from chronomeleon.models.mapping_config import MappingConfig


def _convert_date_or_datetime_to_aware_datetime(source_value: Union[date, datetime], config: MappingConfig) -> datetime:
    """
    returns a datetime object which is aware of the timezone (not naive) and is an exclusive end,
    if the source was an inclusive end
    """
    source_value_datetime: datetime  # a non-naive datetime (exclusive, if end)
    if isinstance(source_value, date):
        if config.source.is_end and config.source.is_inclusive_end:
            source_value_datetime = datetime.combine(source_value + timedelta(days=1), datetime.min.time())
        else:
            source_value_datetime = datetime.combine(source_value, datetime.min.time())
    elif isinstance(source_value, datetime):
        source_value_datetime = source_value
    else:
        raise ValueError(f"source_value must be a date or datetime object but is {source_value.__class__.__name__}")
    if source_value_datetime.tzinfo is None:
        if config.source.implicit_timezone is not None:
            source_value_datetime = config.source.implicit_timezone.localize(source_value_datetime)
        else:
            # pylint:disable=line-too-long
            raise ValueError(
                "source_value must be timezone-aware or implicit_timezone must be set in the mapping configuration"
            )
    source_value_datetime = source_value_datetime.astimezone(pytz.utc)
    return source_value_datetime


def adapt_to_target(source_value: Union[date, datetime], config: MappingConfig) -> datetime:
    """
    maps the source value to a value compatible with the target system by using the given mapping configuration
    """
    if source_value is None:
        raise ValueError("source_value must not be None")
    if config is None:
        raise ValueError("config must not be None")
    if not config.is_self_consistent():
        raise ValueError("config is not self-consistent: " + ", ".join(config.get_consistency_errors()))
    source_value_datetime = _convert_date_or_datetime_to_aware_datetime(source_value, config)
    raise NotImplementedError("not yet implemented")
