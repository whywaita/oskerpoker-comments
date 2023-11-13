import datastore
import utils


def print_timer():
    """Print timer and players for timestamp comment in YouTube"""
    open_flop_time = datastore.get_open_flop_time()
    if open_flop_time == 0:
        return

    p = datastore.get_players()
    print(utils.get_display_elapsed_time(open_flop_time), end=" ")
    print(' vs '.join(p))