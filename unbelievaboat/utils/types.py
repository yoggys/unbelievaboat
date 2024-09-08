from enum import Enum
from typing import Any


class ItemActionType(Enum):
    RESPOND = 1
    ADD_ROLES = 2
    REMOVE_ROLES = 3
    ADD_BALANCE = 4
    REMOVE_BALANCE = 5
    ADD_ITEMS = 6
    REMOVE_ITEMS = 7


class ItemRequirementType(Enum):
    ROLE = 1
    TOTAL_BALANCE = 2
    ITEM = 3


class ItemRequirementMatchType(Enum):
    EVERY = 1
    AT_LEAST_ONE = 2
    NONE = 3


class _MissingSentinel:
    def __eq__(self, other: Any) -> bool:
        return False

    def __bool__(self) -> bool:
        return False


MISSING = _MissingSentinel()
