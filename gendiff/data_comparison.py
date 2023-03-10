"""Compare two dictionaries and return comparison result.

Comparison format:
{key_lvl1: [value_lvl1, comparison_result], ...}

comparison_result in ['added', 'removed', 'changed', 'unchanged']

if comparison_result == 'unchanged':
    value_lvl1 = {key_lvl2: value_lvl2, ...}
elif isinstance(value_lvl1, dict):
    {key_lvl2: [value_lvl2, comparison_result], ...}
else:
    value_lvl2
"""
DIFF_POS = 0
VALUE_POZ = 1
VALUE_UNCHANGED = 'unchanged'
VALUE_REMOVED = 'removed'
VALUE_ADDED = 'added'
VALUE_CHANGED = 'changed'


def generate_diff_dict(
    file1_dict: dict,
    file2_dict: dict,
    result_dict: dict,
) -> dict:
    """Compare two dictionaries and return comparison result.

    Args:
        result_dict: A dictionary with differences.
        file1_dict: The first dictionary to compare.
        file2_dict: The second dictionary to compare.

    Returns:
        The difference dictionary between two dictionaries.
    """
    keys_set = set()
    keys_set.update(file1_dict.keys(), file2_dict.keys())
    for key in keys_set:
        if key not in file2_dict:
            result_dict[key] = [file1_dict[key], VALUE_REMOVED]
            continue
        if key not in file1_dict:
            result_dict[key] = [file2_dict[key], VALUE_ADDED]
            continue
        value1 = file1_dict[key]
        value2 = file2_dict[key]
        if isinstance(value1, dict) and isinstance(value2, dict):
            result_dict[key] = [
                generate_diff_dict(value1, value2, {}),
                VALUE_UNCHANGED,
            ]
            continue
        if value1 == value2:
            result_dict[key] = [value1, VALUE_UNCHANGED]
            continue
        result_dict[key] = [[value1, value2], VALUE_CHANGED]
    return result_dict
