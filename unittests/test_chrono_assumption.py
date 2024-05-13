from datetime import timedelta

import pytest

from chronomeleon.models import ChronoAssumption


@pytest.mark.parametrize(
    "chrono_assumption, is_self_consistent",
    [
        pytest.param(
            ChronoAssumption(resolution=timedelta(days=1)),
            True,
        ),
        pytest.param(
            ChronoAssumption(resolution=timedelta(seconds=1), is_end=True),
            False,
            id="is end without specifying inclusive/exclusive end",
        ),
        pytest.param(
            ChronoAssumption(resolution=timedelta(seconds=1), is_inclusive_end=True),
            False,
            id="inclusive end specified without setting is_end",
        ),
        pytest.param(
            ChronoAssumption(resolution=timedelta(seconds=1), is_inclusive_end=True, is_end=False),
            False,
            id="inclusive end specified with is_end=False",
        ),
    ],
)
def test_self_consistency(chrono_assumption: ChronoAssumption, is_self_consistent: bool):
    assert chrono_assumption.is_self_consistent() == is_self_consistent
