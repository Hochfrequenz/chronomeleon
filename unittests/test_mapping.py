from datetime import date, datetime, timedelta
from typing import Union

import pytest
import pytz

from chronomeleon.mapping import _convert_date_or_datetime_to_aware_datetime
from chronomeleon.models import ChronoAssumption, MappingConfig


@pytest.mark.parametrize(
    "source_value, config, expected",
    [
        pytest.param(
            date(2021, 1, 1),
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1), implicit_timezone=pytz.UTC),
                target=ChronoAssumption(resolution=timedelta(days=1)),
            ),
            datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            id="implicit timezone is set as explicit (date)",
        ),
        pytest.param(
            date(2021, 1, 1),
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1), implicit_timezone=pytz.timezone("Europe/Berlin")),
                target=ChronoAssumption(resolution=timedelta(days=1)),
            ),
            datetime(2020, 12, 31, 23, 0, 0, tzinfo=pytz.UTC),
            id="implicit timezone is set as explicit and converted to UTC afterwards (date)",
        ),
        pytest.param(
            datetime(2021, 1, 1, 0, 0, 0),
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1), implicit_timezone=pytz.timezone("Europe/Berlin")),
                target=ChronoAssumption(resolution=timedelta(days=1)),
            ),
            datetime(2020, 12, 31, 23, 0, 0, tzinfo=pytz.UTC),
            id="implicit timezone is set as explicit and converted to UTC afterwards (datetime)",
        ),
        pytest.param(
            datetime(2021, 6, 1, 0, 0, 0),
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1), implicit_timezone=pytz.timezone("Europe/Berlin")),
                target=ChronoAssumption(resolution=timedelta(days=1)),
            ),
            datetime(2021, 5, 31, 22, 0, 0, tzinfo=pytz.UTC),
            id="implicit timezone is set as explicit and converted to UTC afterwards (datetime)",
        ),
        pytest.param(
            datetime(2021, 5, 31, 0, 0, 0),
            MappingConfig(
                source=ChronoAssumption(
                    resolution=timedelta(days=1),
                    is_end=True,
                    is_inclusive_end=True,
                    implicit_timezone=pytz.timezone("Europe/Berlin"),
                ),
                target=ChronoAssumption(resolution=timedelta(days=1)),
            ),
            datetime(2021, 5, 31, 22, 0, 0, tzinfo=pytz.UTC),
            id="implicit timezone is set as explicit and converted to UTC afterwards (datetime)",
        ),
        pytest.param(
            pytz.timezone("Europe/Berlin").localize(datetime(2021, 5, 31, 0, 0, 0)),
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1), is_end=True, is_inclusive_end=False),
                target=ChronoAssumption(resolution=timedelta(days=1)),
            ),
            datetime(2021, 5, 30, 22, 0, 0, tzinfo=pytz.UTC),
            id="explicit timezone is converted to UTC (datetime)",
        ),
    ],
)
def test_convert_date_or_datetime_to_aware_datetime(
    source_value: Union[datetime, date], config: MappingConfig, expected: datetime
):
    actual = _convert_date_or_datetime_to_aware_datetime(source_value, config)
    assert actual.tzinfo is not None
    assert actual == expected
