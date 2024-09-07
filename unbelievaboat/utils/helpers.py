from typing import Any


class _MissingSentinel:
    def __eq__(self, other: Any) -> bool:
        return False

    def __bool__(self) -> bool:
        return False


MISSING = _MissingSentinel()
