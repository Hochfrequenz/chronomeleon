from datetime import date, datetime, timedelta
from typing import Union

import pytest
import pytz

from chronomeleon.mapping import (
    _convert_aware_datetime_to_target,
    _convert_source_date_or_datetime_to_aware_datetime,
    adapt_to_target,
)
from chronomeleon.models import ChronoAssumption, MappingConfig

_dummy_assumption = ChronoAssumption(resolution=timedelta(days=1))


@pytest.mark.parametrize(
    "source_value, config, expected",
    [
        pytest.param(
            date(2021, 1, 1),
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1), implicit_timezone=pytz.UTC),
                target=_dummy_assumption,
            ),
            datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            id="implicit timezone is set as explicit (date)",
        ),
        pytest.param(
            date(2021, 1, 1),
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1), implicit_timezone=pytz.timezone("Europe/Berlin")),
                target=_dummy_assumption,
            ),
            datetime(2020, 12, 31, 23, 0, 0, tzinfo=pytz.UTC),
            id="implicit timezone is set as explicit and converted to UTC afterwards (date)",
        ),
        pytest.param(
            datetime(2021, 1, 1, 0, 0, 0),
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1), implicit_timezone=pytz.timezone("Europe/Berlin")),
                target=_dummy_assumption,
            ),
            datetime(2020, 12, 31, 23, 0, 0, tzinfo=pytz.UTC),
            id="implicit timezone is set as explicit and converted to UTC afterwards (datetime)",
        ),
        pytest.param(
            datetime(2021, 6, 1, 0, 0, 0),
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1), implicit_timezone=pytz.timezone("Europe/Berlin")),
                target=_dummy_assumption,
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
                target=_dummy_assumption,
            ),
            datetime(2021, 5, 31, 22, 0, 0, tzinfo=pytz.UTC),
            id="implicit timezone is set as explicit and converted to UTC afterwards (datetime)",
        ),
        pytest.param(
            datetime(2021, 5, 31, 0, 0, 0).astimezone(pytz.UTC),
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1), is_end=True, is_inclusive_end=False),
                target=_dummy_assumption,
            ),
            datetime(2021, 5, 30, 22, 0, 0, tzinfo=pytz.UTC),
            id="explicit timezone is converted to UTC (datetime)",
        ),
        pytest.param(
            pytz.utc.localize(datetime(2021, 5, 31, 4, 0, 0)),
            MappingConfig(
                source=ChronoAssumption(
                    resolution=timedelta(days=1),
                    is_end=True,
                    is_inclusive_end=False,
                    is_gastag_aware=True,
                ),
                is_gas=True,
                target=_dummy_assumption,
            ),
            datetime(2021, 5, 30, 22, 0, 0, tzinfo=pytz.UTC),
            id="explicit timezone is converted to UTC (datetime) adapted to _not_ contain the Gastag",
        ),
        pytest.param(
            pytz.utc.localize(datetime(2021, 5, 31, 4, 0, 0)),
            MappingConfig(
                source=ChronoAssumption(
                    resolution=timedelta(days=1),
                    is_end=True,
                    is_inclusive_end=False,
                    is_gastag_aware=True,
                ),
                target=_dummy_assumption,
                is_gas=False,
            ),
            datetime(2021, 5, 31, 4, 0, 0, tzinfo=pytz.UTC),
            id="explicit timezone is converted to UTC (datetime) adapted to _not_ contain the Gastag if its not Gas",
        ),
        pytest.param(
            pytz.utc.localize(datetime(2023, 3, 26, 4, 0, 0)),
            MappingConfig(
                source=ChronoAssumption(
                    resolution=timedelta(days=1),
                    is_end=True,
                    is_inclusive_end=False,
                    is_gastag_aware=True,
                ),
                target=_dummy_assumption,
                is_gas=True,
            ),
            datetime(2023, 3, 25, 23, 0, 0, tzinfo=pytz.UTC),
            id="explicit timezone is converted to UTC (datetime) adapted to contain the Gastag even on DST transitions",
        ),
        pytest.param(
            datetime(2023, 3, 26, 5, 59, 59),
            MappingConfig(
                source=ChronoAssumption(
                    resolution=timedelta(seconds=1),
                    is_end=True,
                    is_inclusive_end=True,
                    is_gastag_aware=True,
                    implicit_timezone=pytz.timezone("Europe/Berlin"),
                ),
                target=_dummy_assumption,
                is_gas=True,
            ),
            datetime(2023, 3, 25, 23, 0, 0, tzinfo=pytz.UTC),
            id="inclusive end is converted to exclusive end on DST transition and with gas tag",
        ),
    ],
)
def test_convert_source_date_or_datetime_to_aware_datetime(
    source_value: Union[datetime, date], config: MappingConfig, expected: datetime
):
    actual = _convert_source_date_or_datetime_to_aware_datetime(source_value, config)  # pylint:disable=protected-access
    assert actual.tzinfo is not None
    assert actual == expected


@pytest.mark.parametrize(
    "intermediate_value, config, expected",
    [
        pytest.param(
            datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            MappingConfig(
                source=_dummy_assumption,
                target=ChronoAssumption(resolution=timedelta(days=1)),
            ),
            datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            id="trivial case",
        ),
        pytest.param(
            datetime(2021, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            MappingConfig(
                source=_dummy_assumption,
                target=ChronoAssumption(resolution=timedelta(days=1), implicit_timezone=pytz.timezone("Europe/Berlin")),
            ),
            pytz.timezone("Europe/Berlin").localize(datetime(2021, 1, 1, 1, 0, 0)),
            id="consider implicit tz (non DST)",
        ),
        pytest.param(
            datetime(2021, 6, 1, 0, 0, 0, tzinfo=pytz.UTC),
            MappingConfig(
                source=_dummy_assumption,
                target=ChronoAssumption(resolution=timedelta(days=1), implicit_timezone=pytz.timezone("Europe/Berlin")),
            ),
            pytz.timezone("Europe/Berlin").localize(datetime(2021, 6, 1, 2, 0, 0)),
            id="consider implicit tz (DST)",
        ),
        pytest.param(
            datetime(2021, 5, 31, 22, 0, 0, tzinfo=pytz.UTC),
            MappingConfig(
                source=_dummy_assumption,
                target=ChronoAssumption(
                    resolution=timedelta(days=1),
                    implicit_timezone=pytz.timezone("Europe/Berlin"),
                    is_gastag_aware=True,
                ),
                is_gas=True,
            ),
            pytz.timezone("Europe/Berlin").localize(datetime(2021, 6, 1, 6, 0, 0)),
            id="DST+implicit TZ+Gastag",
        ),
        pytest.param(
            datetime(2021, 5, 31, 22, 0, 0, tzinfo=pytz.UTC),
            MappingConfig(
                source=_dummy_assumption,
                target=ChronoAssumption(
                    resolution=timedelta(days=1),
                    implicit_timezone=pytz.timezone("Europe/Berlin"),
                    is_gastag_aware=True,
                ),
                is_gas=False,
            ),
            pytz.timezone("Europe/Berlin").localize(datetime(2021, 6, 1, 0, 0, 0)),
            id="DST+implicit TZ+Gastag but not Gas",
        ),
        pytest.param(
            datetime(2021, 5, 31, 22, 0, 0, tzinfo=pytz.UTC),
            MappingConfig(
                source=_dummy_assumption,
                target=ChronoAssumption(
                    resolution=timedelta(milliseconds=1),
                    implicit_timezone=pytz.timezone("Europe/Berlin"),
                    is_gastag_aware=True,
                    is_end=True,
                    is_inclusive_end=True,
                ),
                is_gas=True,
            ),
            pytz.timezone("Europe/Berlin").localize(datetime(2021, 6, 1, 5, 59, 59, 999000)),
            id="DST+implicit TZ+Gastag+inclusive end",
        ),
    ],
)
def test_convert_aware_datetime_to_target(intermediate_value: datetime, config: MappingConfig, expected: datetime):
    actual = _convert_aware_datetime_to_target(intermediate_value, config)
    assert actual == expected


@pytest.mark.parametrize(
    "source_value, config, expected",
    [
        pytest.param(
            date(2024, 1, 1),
            MappingConfig(
                source=ChronoAssumption(
                    resolution=timedelta(days=1),
                    implicit_timezone=pytz.timezone("Europe/Berlin"),
                    is_end=True,
                    is_inclusive_end=False,
                    is_gastag_aware=True,
                ),
                target=ChronoAssumption(
                    resolution=timedelta(microseconds=1),
                    is_end=True,
                    is_inclusive_end=True,
                    is_gastag_aware=False,
                ),
                is_gas=True,
            ),
            datetime(2023, 12, 31, 22, 59, 59, 999999, tzinfo=pytz.UTC),
            # pylint:disable=line-too-long
            id="an exclusive, Gastag aware end**date** with implicit Berlin timezone is converted to an inclusive, Gastag unaware enddate in a system with a 1us resolution",
        ),
        pytest.param(
            date(2023, 12, 31),
            MappingConfig(
                source=ChronoAssumption(
                    resolution=timedelta(days=1),
                    implicit_timezone=pytz.timezone("Europe/Berlin"),
                    is_end=True,
                    is_inclusive_end=True,
                    is_gastag_aware=True,
                ),
                target=ChronoAssumption(
                    resolution=timedelta(days=1),
                    is_end=True,
                    is_inclusive_end=False,
                    is_gastag_aware=False,
                ),
                is_gas=True,
            ),
            datetime(2023, 12, 31, 23, 0, 0, 0, tzinfo=pytz.UTC),
            # pylint:disable=line-too-long
            id="an inclusive, Gastag aware enddate with implicit Berlin timezone is converted to an exclusive, Gastag aware enddate in a system with a 1d resolution",
        ),
        pytest.param(
            datetime(2034, 4, 5, 6, 7, 8),
            MappingConfig(
                source=ChronoAssumption(
                    resolution=timedelta(days=1),
                    implicit_timezone=pytz.timezone("Europe/Berlin"),
                    is_end=True,
                    is_inclusive_end=True,
                    is_gastag_aware=True,
                ),
                target=ChronoAssumption(
                    resolution=timedelta(days=1),
                    implicit_timezone=pytz.timezone("Europe/Berlin"),
                    is_end=True,
                    is_inclusive_end=True,
                    is_gastag_aware=True,
                ),
                is_gas=True,
            ),
            pytz.timezone("Europe/Berlin").localize(datetime(2034, 4, 5, 6, 7, 8)),
            id="source==target converts implicit TZ to explicit TZ",
        ),
    ],
)
def test_mapping_a_datetime(source_value: datetime, config: MappingConfig, expected: datetime):
    actual = adapt_to_target(source_value, config)
    assert actual == expected
