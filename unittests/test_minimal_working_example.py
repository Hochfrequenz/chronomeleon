"""
a MWE test for demo purposes
"""

from datetime import date, datetime, timedelta

import pytz

from chronomeleon import ChronoAssumption, MappingConfig, adapt_to_target


def test_mwe():
    config = MappingConfig(  # make assumptions explicit
        source=ChronoAssumption(
            implicit_timezone=pytz.timezone("Europe/Berlin"),
            resolution=timedelta(days=1),
            is_inclusive_end=True,
            is_gastag_aware=False,
        ),
        target=ChronoAssumption(resolution=timedelta(milliseconds=1), is_inclusive_end=True, is_gastag_aware=True),
        is_end=True,
        is_gas=True,
    )
    source_value = date(2021, 12, 31)
    result = adapt_to_target(source_value, config)  # do the mapping
    assert result == datetime(2022, 1, 1, 4, 59, 59, microsecond=999000, tzinfo=pytz.utc)
