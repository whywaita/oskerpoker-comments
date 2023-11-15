import typing
import Levenshtein


def get_correct_player_name(correct_dictonary: typing.List[str], raw: str) -> str:
    """Get correct player name from raw string.

    Args:
        correct_dictonary (typing.List[str]): The list of correct player name.
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
    if raw in correct_dictonary:
        return raw

    # Fix the typo using Levenshtein distance
    distances = []
    for correct in correct_dictonary:
        distances.append(Levenshtein.distance(raw, correct))
    min_distance = min(distances)
    min_distance_index = distances.index(min_distance)
    return correct_dictonary[min_distance_index]
