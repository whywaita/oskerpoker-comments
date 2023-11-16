import typing

import movieparser.datastore
import movieparser.utils


def print_timer():
    """Print timer and players for timestamp comment in YouTube"""
    open_flop_time = movieparser.datastore.get_open_flop_time()
    if open_flop_time == 0:
        return

    p = movieparser.datastore.get_players()
    print(movieparser.utils.get_display_elapsed_time(open_flop_time), end=" ")
    print(' vs '.join(p))


def get_timestamp_comment_from_list(flop_times: typing.List[movieparser.datastore.FlopTime]) -> str:
    """Generate timestamp comment from list of FlopTime"""
    if not flop_times:
        return ""

    comment = ""
    for flop_time in flop_times:
        comment += movieparser.utils.get_display_elapsed_time(flop_time.time) + " "
        comment += ' vs '.join(flop_time.players) + "\n"

    return comment


def print_timer_from_list(flop_times: typing.List[movieparser.datastore.FlopTime]):
    """Print timer and players for timestamp comment in YouTube"""
    out = get_timestamp_comment_from_list(flop_times)
    print(out)


def get_stored_flop_time() -> movieparser.datastore.FlopTime:
    open_flop_time = movieparser.datastore.get_open_flop_time() - 1000
    p = movieparser.datastore.get_players()

    ft = movieparser.datastore.FlopTime(open_flop_time, p)
    return ft
