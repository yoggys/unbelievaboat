from typing import Dict, Union, List


class Permission:
    economy: int = 1

    def __init__(self, allow: int) -> None:
        self.allow: int = allow

    def __str__(self) -> str:
        return "<Permission allow={}>".format(self.allow)

    @property
    def json(self) -> Dict[str, bool]:
        json: Dict[str, bool] = {}
        for permission in vars(self.__class__).keys():
            if not permission.startswith("__"):
                json[permission] = bool(
                    self.allow & getattr(self.__class__, permission)
                )
        return json

    def has(self, permissions: Union[str, List[str]]) -> bool:
        if isinstance(permissions, list):
            return all(
                bool(self.allow & getattr(self.__class__, perm)) for perm in permissions
            )
        else:
            return bool(self.allow & getattr(self.__class__, permissions))
