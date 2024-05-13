from datetime import timedelta

import pytest

from chronomeleon.models import ChronoAssumption, MappingConfig


@pytest.mark.parametrize(
    "mapping_config, is_self_consistent",
    [
        pytest.param(
            MappingConfig(
                source=ChronoAssumption(resolution=timedelta(days=1)),
                target=ChronoAssumption(resolution=timedelta(days=2)),
            ),
            True,
        ),
        pytest.param(
            MappingConfig(
                source=ChronoAssumption(
                    resolution=timedelta(days=1), is_end=True, is_inclusive_end=True, is_gastag_aware=True
                ),
                target=ChronoAssumption(
                    resolution=timedelta(seconds=1), is_end=True, is_inclusive_end=True, is_gastag_aware=False
                ),
            ),
            True,
        ),
    ],
)
def test_self_consistency(mapping_config: MappingConfig, is_self_consistent: bool):
    assert mapping_config.is_self_consistent() == is_self_consistent
