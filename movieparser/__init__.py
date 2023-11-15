import typing
import cv2
import sys

from movieparser.cli import print_timer, get_stored_flop_time, print_timer_from_list
from movieparser.cv import is_open_flop, get_players_frame
from movieparser.datastore import (
    Status,
    FlopTime,
    get_now_status,
    get_open_flop_time,
    get_open_flop_time,
    get_players,
    add_player
)
from movieparser.utils import get_display_elapsed_time, is_check_early_close, sanitize_player_name
from movieparser.stage import become_open_flop, next_game


def parse_movie(file_path: str, delay=1, window_name='frame', debug=False) -> typing.List[FlopTime]:
    flop_time_list = []

    print(file_path)
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        sys.exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if int(cap.get(cv2.CAP_PROP_POS_MSEC)) % 1000 != 0:
            continue

        frame = cv2.resize(frame, dsize=(1280, 720))
        is_opened = is_open_flop(frame)

        if is_opened & (get_now_status() == Status.PRE_FLOP):
            if debug:
                print("become_open_flop")
            become_open_flop(cap.get(cv2.CAP_PROP_POS_MSEC))

        if (is_opened is False) & (get_now_status() == Status.OPEN_FLOP):
            if is_check_early_close(cap.get(cv2.CAP_PROP_POS_MSEC)):
                if debug:
                    print("early close")
                continue
            if debug:
                print("next_game")

            ft = get_stored_flop_time()
            flop_time_list.append(ft)
            next_game()

        if (is_opened
                & (get_now_status() == Status.OPEN_FLOP)
                & (len(get_players()) == 0)
        ):
            if debug:
                print("not yet load players. become to load players")

            players = get_players_frame(frame)
            if len(players) != 0:
                # FOUND_TIME = get_display_elapsed_time(cap.get(cv2.CAP_PROP_POS_MSEC) - 1000)
                for player in players:
                    sanitized_player = sanitize_player_name(player)
                    add_player(sanitized_player)

        if debug:
            cv2.imshow(window_name, frame)

        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    if debug:
        cv2.destroyWindow(window_name)

    return flop_time_list
