"""
This a docstring for the module.
"""

import datetime as dt_module
from datetime import date, datetime, timedelta
from typing import Union

import pytz

from chronomeleon.models.mapping_config import MappingConfig

_berlin = pytz.timezone("Europe/Berlin")


def _convert_source_date_or_datetime_to_aware_datetime(
    source_value: Union[date, datetime], config: MappingConfig
) -> datetime:
    """
    returns a datetime object which is aware of the timezone (i.e. not naive) and is an exclusive end
    regardless of whether the source was configured as an inclusive or exclusive end.
    """
    source_value_datetime: datetime  # a non-naive datetime (exclusive, if end)
    if isinstance(source_value, datetime):
        source_value_datetime = source_value
        if config.is_end and config.source.is_inclusive_end:
            assert config.source.resolution is not None  # ensured by the consistency check
            source_value_datetime += config.source.resolution
    elif isinstance(source_value, date):
        if config.is_end and config.source.is_inclusive_end:
            source_value_datetime = datetime.combine(source_value + timedelta(days=1), datetime.min.time())
        else:
            source_value_datetime = datetime.combine(source_value, datetime.min.time())
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
    if config.source.is_gastag_aware and config.is_gas:
        berlin_local_datetime = source_value_datetime.astimezone(_berlin)
        if berlin_local_datetime.time() == dt_module.time(6, 0, 0):
            berlin_local_datetime = berlin_local_datetime.replace(hour=0).replace(tzinfo=None)
            # We need to re-localize the datetime, because the UTC offset might have changed
            # The Gastag does not always start 6h after midnight.
            # It might also be 5h or 7h on DST transition days.
            berlin_local_datetime = _berlin.localize(berlin_local_datetime)
            source_value_datetime = berlin_local_datetime.astimezone(pytz.utc)
    return source_value_datetime


def _convert_aware_datetime_to_target(value: datetime, config: MappingConfig) -> datetime:
    """
    returns a date or datetime object which is compatible with the target system
    """
    if value.tzinfo is None:
        raise ValueError("value must be timezone-aware at this point")
    target_value: datetime = value
    if config.target.is_gastag_aware and config.is_gas:
        _berlin_local_datetime = value.astimezone(_berlin)
        if _berlin_local_datetime.time() == dt_module.time(0, 0, 0):
            _berlin_local_datetime = _berlin_local_datetime.replace(hour=6).replace(tzinfo=None)
            # We need to re-localize the datetime, because the UTC offset might have changed.
            # The Gastag does not always start 6h after midnight.
            # It might also be 5h or 7h on DST transition days.
            _berlin_local_datetime = _berlin.localize(_berlin_local_datetime)
            target_value = _berlin_local_datetime.astimezone(pytz.utc)
    if config.is_end and config.target.is_inclusive_end:
        assert config.target.resolution is not None  # ensured by the consistency check
        target_value = target_value - config.target.resolution  # converts the exclusive end to an inclusive end
        # and e.g. 2024-01-02 00:00:00 to 2024-01-01 23:59:59 if the resolution is timedelta(seconds=1)
        # Work because the original value is - if it is an end - always an exclusive end.
    if config.target.implicit_timezone is not None:
        target_value = target_value.astimezone(config.target.implicit_timezone)
    if config.target.is_date_only:
        target_value = datetime.combine(target_value.date(), datetime.min.time())
    return target_value


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
    # there are just 2 steps:
    # 1. convert the source from whatever it is to something unified with what we can work
    # 2. convert the unified source to the target (which might be just as obscure as the source)
    source_value_datetime = _convert_source_date_or_datetime_to_aware_datetime(source_value, config)  # step 1
    assert source_value_datetime.tzinfo is not None
    assert source_value_datetime.tzinfo == pytz.utc
    target_value = _convert_aware_datetime_to_target(source_value_datetime, config)  # step 2
    return target_value
