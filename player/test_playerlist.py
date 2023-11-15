import pytest

from player.playerlist import generate_player_list


@pytest.mark.parametrize('player_comments, expected', [
    ('''
        00:01:35 FOO vs BAR
        00:01:50 FOO vs BAZ
        00:02:50 BAX vs BAZ
    ''', ['BAR', 'BAX', 'BAZ', 'FOO']),
])
def test_generate_player_list(player_comments, expected):
    assert generate_player_list(player_comments) == expected
