import ast
import argparse
import sys
import typing
import os
import concurrent.futures

import movieparser
import player
import web


def command_parse_movie(input_args: argparse.Namespace):
    flop_time_list = movieparser.parse_movie(
        input_args.file_path,
        input_args.delay,
        input_args.window_name,
        input_args.debug)
    movieparser.print_timer_from_list(flop_time_list)


def command_get_player_name(input_args: argparse.Namespace):  # pylint: disable=unused-argument
    raw_data = sys.stdin.read()
    player_name = player.generate_player_list(raw_data)
    print(player_name)


def command_autofix_player_name(input_args: argparse.Namespace):
    correct_player_name = input_args.correct_player_name

    raw_data = sys.stdin.read()
    fixed = player.autofix_timestamp_comment(raw_data, correct_player_name)

    print(fixed)


def command_launch_webserver(input_args: argparse.Namespace):  # pylint: disable=unused-argument
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    executor.submit(web.web.execute_queue)
    port = os.environ.get('PORT', 5050)
    web.app.run(port=port, host='0.0.0.0')


def parse_str_list(input_str: str) -> typing.List[str]:
    try:
        input_list = ast.literal_eval(input_str)
        if not isinstance(input_list, list) or not all(isinstance(i, str) for i in input_list):
            raise argparse.ArgumentTypeError("Input should be a list of strings.")
        return input_list
    except ValueError as e:
        raise argparse.ArgumentTypeError("Input should be a list of strings.") from e


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_parse_movie = subparsers.add_parser('parse-movie')
    parser_parse_movie.description = 'Parse movie and generate timestamp comment.'
    parser_parse_movie.add_argument('--file_path', type=str, required=True)
    parser_parse_movie.add_argument('--delay', type=int, default=1)
    parser_parse_movie.add_argument('--window_name', type=str, default='frame')
    parser_parse_movie.add_argument('--debug', type=bool, default=False)
    parser_parse_movie.set_defaults(handler=command_parse_movie)

    parser_get_player_name = subparsers.add_parser('get-player-name')
    parser_get_player_name.description = 'Get player name from output of `parse-movie`.'
    parser_get_player_name.set_defaults(handler=command_get_player_name)

    parser_autofix_player_name = subparsers.add_parser('autofix-player-name')
    parser_autofix_player_name.description = 'Autofix player name from output of `parse-movie`.'
    parser_autofix_player_name.add_argument(
        '--correct-player-name',
        type=parse_str_list,
        required=True
    )
    parser_autofix_player_name.set_defaults(handler=command_autofix_player_name)

    parser_launch_webserver = subparsers.add_parser('launch-webserver')
    parser_launch_webserver.description = 'Launch webserver.'
    parser_launch_webserver.set_defaults(handler=command_launch_webserver)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
