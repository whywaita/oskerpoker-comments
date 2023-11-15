import movieparser.datastore


def become_open_flop(elapsed_time_ms: float):
    movieparser.datastore.set_now_status(movieparser.datastore.Status.OPEN_FLOP)
    movieparser.datastore.set_open_flop_time(elapsed_time_ms)


def next_game():
    movieparser.datastore.reset_store_data()
