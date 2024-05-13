"""contains the Mapping configuration class"""

from dataclasses import dataclass
from typing import Optional

from .chrono_assumption import ChronoAssumption


@dataclass(frozen=True, kw_only=True)
class MappingConfig:
    """
    represents the mapping rules for one date(time) field from one system to another
    """

    source: ChronoAssumption
    """
    assumptions about the interpretation of the date(time) field in the source system
    """
    target: ChronoAssumption
    """
    assumptions about the interpretation of the date(time) field in the source system
    """

    is_end: Optional[bool] = None
    """
    True if and only if the date or time is the end of a range. None if it doesn't matter.
    """

    is_gas: Optional[bool] = None
    """
    True if the sparte is Gas.
    Set to true to trigger the gas tag modifications in source, target or both, if necessary. Ignore otherwise.
    """

    def get_consistency_errors(self) -> list[str]:
        """
        returns a list of error messages if the mapping configuration is not self-consistent
        """
        errors: list[str] = []
        if not isinstance(self.source, ChronoAssumption):
            errors.append("source must be a ChronoAssumption object")
        else:
            errors.extend(["source: " + x for x in self.source.get_consistency_errors()])
        if not isinstance(self.target, ChronoAssumption):
            errors.append("target must be a ChronoAssumption object")
        else:
            errors.extend(["target: " + x for x in self.target.get_consistency_errors()])
        if (self.source.is_gastag_aware or self.target.is_gastag_aware) and self.is_gas is None:
            errors.append("if is_gastag_aware is set in either source or target, then is_gas must not be None")
            # The opposite is not the case: I can set is_gas to True without setting is_gastag_aware to True
        if (
            self.source.is_inclusive_end is not None or self.target.is_inclusive_end is not None
        ) and self.is_end is None:
            errors.append("if is_inclusive_end is set in either source or target, then is_end must not be None")
        if self.is_end is True and (self.source.is_inclusive_end is None or self.target.is_inclusive_end is None):
            errors.append("if is_end is True, then is_inclusive_end must not be None in both source and target")
        return errors

    def is_self_consistent(self) -> bool:
        """
        checks if the mapping configuration is self-consistent
        """
        return not any(self.get_consistency_errors())
