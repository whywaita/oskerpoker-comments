import typing
import re


def generate_player_list(player_comments: str) -> typing.List[str]:
    """Generate player dict from a given output string.

    Args:
        player_comments (str): The output string from oskerpoker-comments.
    Returns:
        str: The list of player name.

    Example:
        >>> generate_player_list(
        ... '''
        ... 00:01:35 FOO vs BAR
        ... 00:01:50 FOO vs BAZ
        ... 00:02:50 BAX vs BAZ
        ... ''')

        ['BAR', 'BAX', 'BAZ', 'FOO']
    """

    players = []

    for line in player_comments.split('\n'):
        if not line:
            continue
        line = re.sub(r'^(\d{2}):(\d{2}):(\d{2})', '', line.strip()).strip()
        ps = line.split(' vs ')
        for p in ps:
            if p and p not in players:
                players.append(p)

    players.sort()
    return players
