import typing
import re
import Levenshtein


def get_correct_player_name(correct_dictionary: typing.List[str], raw: str) -> str:
    """Get correct player name from raw string.

    Args:
        correct_dictionary (typing.List[str]): The list of correct player name.
        raw (str): The raw string.

    Returns:
        str: The correct player name.

    Example:
        Found extact match.
        >>> get_correct_player_name(
        ...     ['FOO', 'BAR', 'BAZ'],
        ...     'BAR'
        ... )
        'FOO'

        Fix the typo.
        >>> get_correct_player_name(
        ...     ['FOO', 'BAR', 'BAZ'],
        ...     'FO0'
        ... )
        'FOO'
    """

    # Found exact match
    if raw in correct_dictionary:
        return raw

    # Fix the typo using Levenshtein distance
    distances = []
    for correct in correct_dictionary:
        distances.append(Levenshtein.distance(raw, correct))
    min_distance = min(distances)
    min_distance_index = distances.index(min_distance)
    return correct_dictionary[min_distance_index]


def autofix_timestamp_comment(timestamp_comment: str, correct_player_name: typing.List[str]) -> str:
    need_replace = []

    fixed = timestamp_comment

    for line in timestamp_comment.split('\n'):
        if not line:
            continue
        line = line.strip()
        # 00:00:00 FOO vs BAR
        for value in line.split(' '):
            value = value.strip()
            if re.match(r'^\d{2}:\d{2}:\d{2}$', value):
                # timestamp don't need to fix
                continue
            if re.match(r'^vs$', value):
                # vs don't need to fix
                continue
            found_name = get_correct_player_name(correct_player_name, value)
            if value != found_name:
                print(f'{value} -> {found_name}')
                need = {'need_fix_value': value, 'correct_name': found_name}
                if value in [d.get('need_fix_value') for d in need_replace]:
                    # already exist
                    continue
                need_replace.append(need)

    for need in need_replace:
        value = need['need_fix_value']
        found_name = need['correct_name']
        fixed = fixed.replace(' '+value+' ', ' '+found_name+' ')
        fixed = fixed.replace(' '+value+'\n', ' '+found_name+'\n')

    return fixed
