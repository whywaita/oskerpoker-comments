import pytest

from player.fixname import get_correct_player_name


@pytest.mark.parametrize('correct_players, input_name, expected', [
    (['FOO', 'BAR', 'BAZ'], 'BAR', 'BAR'),
    (['FOO', 'BAR', 'BAZ'], 'FO0', 'FOO'),
])
def test_get_correct_player_name(correct_players, input_name, expected):
    assert get_correct_player_name(correct_players, input_name) == expected