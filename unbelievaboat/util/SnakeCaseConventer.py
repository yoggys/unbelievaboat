import re
from typing import Any, Union, Dict, List


def to_snake_case_deep(
    data: Union[Dict[str, Any], List[Any], Any]
) -> Union[Dict[str, Any], List[Any], Any]:
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower()
            new_data[new_key] = to_snake_case_deep(value)
        return new_data
    elif isinstance(data, list):
        return [to_snake_case_deep(item) for item in data]
    else:
        return data
