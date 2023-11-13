import sys
import argparse
import cv2

import cv
import cli
import datastore
import stage
import utils


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, required=True)
    parser.add_argument('--delay', type=int, default=1)
    parser.add_argument('--window_name', type=str, default='frame')
    parser.add_argument('--debug', type=bool, default=False)
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.file_path)
    if not cap.isOpened():
        sys.exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if int(cap.get(cv2.CAP_PROP_POS_MSEC)) % 1000 != 0:
            continue

        frame = cv2.resize(frame, dsize=(1280, 720))
        IS_OPENED = cv.is_open_flop(frame)

        if IS_OPENED & (datastore.get_now_status() == datastore.Status.PRE_FLOP):
            if args.debug:
                print("become_open_flop")
            stage.become_open_flop(cap.get(cv2.CAP_PROP_POS_MSEC))

        if (IS_OPENED is False) & (datastore.get_now_status() == datastore.Status.OPEN_FLOP):
            if utils.is_check_early_close(cap.get(cv2.CAP_PROP_POS_MSEC)):
                if args.debug:
                    print("early close")
                continue
            if args.debug:
                print("next_game")
            cli.print_timer()
            stage.next_game()

        if (IS_OPENED
                & (datastore.get_now_status() == datastore.Status.OPEN_FLOP)
                & (len(datastore.get_players()) == 0)
        ):
            if args.debug:
                print("not yet load players. become to load players")

            players = cv.get_players_frame(frame)
            if len(players) != 0:
                FOUND_TIME = utils.get_display_elapsed_time(cap.get(cv2.CAP_PROP_POS_MSEC) - 1000)
                for player in players:
                    sanitized_player = utils.sanitize_player_name(player)
                    datastore.add_player(sanitized_player)

        if args.debug:
            cv2.imshow(args.window_name, frame)

        if cv2.waitKey(args.delay) & 0xFF == ord('q'):
            break

    if args.debug:
        cv2.destroyWindow(args.window_name)
