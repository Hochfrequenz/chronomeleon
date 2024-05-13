from datetime import timedelta

import pytest

from chronomeleon import ChronoAssumption


@pytest.mark.parametrize(
    "chrono_assumption, is_self_consistent",
    [
        pytest.param(
            ChronoAssumption(resolution=timedelta(days=1)),
            True,
        ),
    ],
)
def test_self_consistency(chrono_assumption: ChronoAssumption, is_self_consistent: bool):
    assert chrono_assumption.is_self_consistent() == is_self_consistent
