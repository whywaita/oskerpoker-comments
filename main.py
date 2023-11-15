import argparse

import movieparser


def command_parse_movie(args: argparse.Namespace):
    flop_time_list = movieparser.parse_movie(args.file_path, args.delay, args.window_name, args.debug)
    movieparser.print_timer_from_list(flop_time_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_parse_movie = subparsers.add_parser('parse-movie')
    parser_parse_movie.add_argument('--file_path', type=str, required=True)
    parser_parse_movie.add_argument('--delay', type=int, default=1)
    parser_parse_movie.add_argument('--window_name', type=str, default='frame')
    parser_parse_movie.add_argument('--debug', type=bool, default=False)
    parser_parse_movie.set_defaults(handler=command_parse_movie)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
